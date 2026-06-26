#!/bin/bash
set -e

if [ $# -lt 1 ]; then
    echo "ERROR: Please provide build directory path"
    echo "Usage: $0 <build_directory>"
    exit 1
fi

BUILD_DIR="$1"
if [[ "$BUILD_DIR" != /* ]]; then
    BUILD_DIR="$(cd "$(dirname "$0")" && cd "$BUILD_DIR" && pwd)"
else
    BUILD_DIR="$(cd "$BUILD_DIR" && pwd)"
fi

FLASH_ARGS_FILE="${BUILD_DIR}/flash_args"
OUTPUT_DIR="${BUILD_DIR}/firmware_package"
ZIP_NAME="esp_firmware_$(date +%Y%m%d_%H%M%S).zip"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ESPTOOL_WIN_DIR="tools/esptool"
ESPTOOL_SOURCE="${SCRIPT_DIR}/esptool/esptool.exe"

if [ ! -d "${BUILD_DIR}" ]; then
    echo "ERROR: Build directory not found: ${BUILD_DIR}"
    exit 1
fi

if [ ! -f "${FLASH_ARGS_FILE}" ]; then
    echo "ERROR: flash_args file not found: ${FLASH_ARGS_FILE}"
    exit 1
fi

mkdir -p "${OUTPUT_DIR}"

echo "Build directory: ${BUILD_DIR}"
echo "Parsing flash_args..."

FLASH_PARAMS=$(head -1 "${FLASH_ARGS_FILE}")

FIRMWARE_LIST=""
WIN_FIRMWARE_ARGS=""
while read -r line; do
    [ -z "$line" ] && continue
    addr=$(echo "$line" | awk '{print $1}')
    file=$(echo "$line" | awk '{print $2}')
    filename=$(basename "$file")
    FIRMWARE_LIST="${FIRMWARE_LIST}        ${addr} ${filename} \\\n"
    WIN_FIRMWARE_ARGS="${WIN_FIRMWARE_ARGS} ${addr} ${filename}"
done < <(tail -n +2 "${FLASH_ARGS_FILE}")

echo "Generating flash scripts..."

cat > "${OUTPUT_DIR}/flash.sh" << SCRIPT_EOF
#!/bin/bash
set -e
BAUD="460800"
CHIP="esp32s2"
ESPTOOL="esptool.py"
MAC_RECORD_FILE="mac_addresses.txt"
READ_MAC_ONLY=0

while [[ "$1" == "--read-mac" ]]; do
    READ_MAC_ONLY=1
    shift
done

record_mac() {
    local PORT=\$1
    local DEVICE_NAME=\$(basename "\$PORT")
    local MAC_LOG="/tmp/read_mac_\${DEVICE_NAME}.log"
    local MAC_CLEAN
    if ! \${ESPTOOL} --chip \${CHIP} -p \${PORT} -b \${BAUD} read_mac > "\${MAC_LOG}" 2>&1; then
        echo "[\${DEVICE_NAME}] Warning: failed to read MAC" >&2
        return 1
    fi
    MAC_CLEAN=\$(grep -Eo '([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}' "\${MAC_LOG}" | head -n 1 | tr -d ':' | tr '[:upper:]' '[:lower:]')
    [ -z "\${MAC_CLEAN}" ] && return 1
    touch "\${MAC_RECORD_FILE}"
    if ! grep -Fxq "\${MAC_CLEAN}" "\${MAC_RECORD_FILE}"; then
        echo "\${MAC_CLEAN}" >> "\${MAC_RECORD_FILE}"
    fi
}

record_mac_from_log() {
    local LOG_FILE=\$1
    local DEVICE_NAME=\$2
    local MAC_RAW
    local MAC_CLEAN

    MAC_RAW=\$(grep -Eo '([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}' "\${LOG_FILE}" | head -n 1)
    if [ -z "\${MAC_RAW}" ]; then
        echo "[\${DEVICE_NAME}] Warning: MAC not found in flash log"
        return 1
    fi

    MAC_CLEAN=\$(echo "\${MAC_RAW}" | tr -d ':' | tr '[:upper:]' '[:lower:]')
    touch "\${MAC_RECORD_FILE}"
    if ! grep -Fxq "\${MAC_CLEAN}" "\${MAC_RECORD_FILE}"; then
        echo "\${MAC_CLEAN}" >> "\${MAC_RECORD_FILE}"
        echo "[\${DEVICE_NAME}] MAC recorded: \${MAC_CLEAN}"
    else
        echo "[\${DEVICE_NAME}] MAC already exists: \${MAC_CLEAN}"
    fi
}

flash_single() {
    local PORT=\$1
    local DEVICE_NAME=\$(basename "\$PORT")
    echo "[\${DEVICE_NAME}] Flashing..."
    if [ ! -e "\${PORT}" ]; then
        echo "[\${DEVICE_NAME}] ERROR: Port not found: \${PORT}"
        return 1
    fi
    local LOG_FILE="/tmp/flash_\${DEVICE_NAME}.log"
    local RETRY=0
    local MAX_RETRY=3
    while [ \$RETRY -lt \$MAX_RETRY ]; do
        RETRY=\$((RETRY + 1))
        echo "[\${DEVICE_NAME}] Attempt \${RETRY}/\${MAX_RETRY}..."
        if \${ESPTOOL} --chip \${CHIP} -p \${PORT} -b \${BAUD} \\
            --before=default_reset --after=no_reset --no-stub write_flash \\
${FIRMWARE_LIST}            > "\${LOG_FILE}" 2>&1; then
            echo "[\${DEVICE_NAME}] Flash OK"
            record_mac_from_log "\${LOG_FILE}" "\${DEVICE_NAME}" || true
            return 0
        fi
        if [ \$RETRY -lt \$MAX_RETRY ]; then
            echo "[\${DEVICE_NAME}] Retry in 2 seconds..."
            sleep 2
        fi
    done
    echo "[\${DEVICE_NAME}] Flash FAILED! Log: \${LOG_FILE}"
    return 1
}

if [ \${READ_MAC_ONLY} -eq 1 ]; then
    OP_FUNC=record_mac
else
    OP_FUNC=flash_single
fi

ALL_PORTS=()
for arg in "\$@"; do
    if [[ "\$arg" == *"*"* ]] || [[ "\$arg" == *"?"* ]]; then
        for port in \$arg; do
            [ -e "\$port" ] && ALL_PORTS+=("\$port")
        done
    else
        [ -e "\$arg" ] && ALL_PORTS+=("\$arg") || echo "Warning: Port not found: \$arg"
    fi
done

if [ \${#ALL_PORTS[@]} -eq 0 ]; then
    ALL_PORTS=("/dev/ttyUSB0")
fi

if [ \${#ALL_PORTS[@]} -eq 1 ]; then
    ${OP_FUNC} "\${ALL_PORTS[0]}"
else
    PIDS=()
    FAILED=()
    for PORT in "\${ALL_PORTS[@]}"; do
        ${OP_FUNC} "\$PORT" &
        PIDS+=(\$!)
    done
    for i in "\${!PIDS[@]}"; do
        if ! wait "\${PIDS[\$i]}"; then
            FAILED+=("\${ALL_PORTS[\$i]}")
        fi
    done
    if [ \${#FAILED[@]} -gt 0 ]; then
        echo "Failed: \${FAILED[*]}"
        exit 1
    fi
fi
SCRIPT_EOF
chmod +x "${OUTPUT_DIR}/flash.sh"

cat > "${OUTPUT_DIR}/flash_one.bat" << WIN_ONE_EOF
@echo off
setlocal enabledelayedexpansion
set "BAUD=460800"
set "CHIP=esp32s2"
set "ESPTOOL=tools\esptool\esptool.exe"
set "FLASH_PARAMS=${FLASH_PARAMS}"
set "MAC_RECORD_FILE=mac_addresses.txt"
set "READ_MAC=0"
set "PORT=%~1"
if /I "%~1"=="--read-mac" (
    set "READ_MAC=1"
    set "PORT=%~2"
)
if "%PORT%"=="" set "PORT=COM1"
if not exist "%ESPTOOL%" (
    echo ERROR: esptool.exe not found
    exit /b 1
)
if %READ_MAC%==1 (
    call :record_mac
    exit /b 0
)
set /a RETRY=0
set /a MAX_RETRY=3
:retry
set /a RETRY+=1
echo [%PORT%] Attempt %RETRY%/%MAX_RETRY%...
"%ESPTOOL%" --chip %CHIP% -p %PORT% -b %BAUD% --before=default_reset --after=no_reset --no-stub write_flash %FLASH_PARAMS%${WIN_FIRMWARE_ARGS}
if %errorlevel%==0 (
    echo [%PORT%] Flash OK
    call :record_mac
    exit /b 0
)
if %RETRY% LSS %MAX_RETRY% (
    timeout /t 2 /nobreak >nul
    goto retry
)
exit /b 1

:record_mac
set "MAC_OUT=%TEMP%\mo_%RANDOM%.txt"
set "PSCMD=%ESPTOOL% --chip %CHIP% -p %PORT% -b %BAUD% read_mac"
echo [%PORT%] Reading MAC...
powershell -NoProfile -ExecutionPolicy Bypass -Command "!PSCMD! 2>&1 | Select-String -Pattern '([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}' | Select-Object -First 1 | ForEach-Object { \$_.Matches.Value.Replace(':','').ToLower() } | Out-File -FilePath '!MAC_OUT!' -Encoding ASCII -NoNewline"
echo -----------------------------------
if exist "!MAC_OUT!" (
    set /p MAC_CLEAN=<"!MAC_OUT!"
    echo [DEBUG] Raw MAC from file: !MAC_CLEAN!
) else (
    echo [ERROR] File !MAC_OUT! does not exist.
)
del "%MAC_OUT%" 2>nul
if not defined MAC_CLEAN goto :eof
if not exist "%MAC_RECORD_FILE%" type nul > "%MAC_RECORD_FILE%"
findstr /I /X /C:"!MAC_CLEAN!" "%MAC_RECORD_FILE%" >nul 2>nul
if errorlevel 1 echo(!MAC_CLEAN!>>"%MAC_RECORD_FILE%"
goto :eof
WIN_ONE_EOF

cat > "${OUTPUT_DIR}/flash.bat" << WIN_MAIN_EOF
@echo off
setlocal enabledelayedexpansion
set "PORTS="
set "SINGLE_PORT="
set "MODE=flash"

REM Parse arguments
if /I "%~1"=="--read-mac" (
    set "MODE=--read-mac"
    shift
)
if /I "%~1"=="all" (
    for /f "tokens=3" %%a in ('reg query HKLM\HARDWARE\DEVICEMAP\SERIALCOMM 2^>nul ^| findstr /I "COM"') do (
        set "PN=%%a"
        set "PN=!PN:\\0=!"
        set "PN=!PN: =!"
        if not "!PN!"=="" set "PORTS=!PORTS! !PN!"
    )
    if "!PORTS!"=="" exit /b 1
    goto multi
)

if "%~2"=="" (
    set "SINGLE_PORT=%~1"
    goto single
)

REM Collect ports from args
:collect
if "%~1"=="" goto done_collect
set "PORTS=!PORTS! %~1"
shift
goto collect
:done_collect

if not "!PORTS!"=="" goto multi
exit /b 1

:single
if "!SINGLE_PORT!"=="" exit /b 1
if "!MODE!"=="--read-mac" (
    call flash_one.bat --read-mac !SINGLE_PORT!
) else (
    call flash_one.bat !SINGLE_PORT!
)
exit /b %errorlevel%

:multi
for %%P in (!PORTS!) do (
    echo [%%P] Starting flash...
    if "!MODE!"=="--read-mac" (
        start /b "Flash %%P" cmd /c "cd /d %~dp0 && call flash_one.bat --read-mac %%P"
    ) else (
        start /b "Flash %%P" cmd /c "cd /d %~dp0 && call flash_one.bat %%P"
    )
)
goto wait

:wait
timeout /t 1 /nobreak >nul
tasklist /fi "imagename eq esptool.exe" /fo csv 2>nul | findstr /i "esptool.exe" >nul
if %errorlevel%==0 goto wait
exit /b 0
WIN_MAIN_EOF



echo "Windows scripts generated"

echo "Copying firmware files..."
while read -r line; do
    [ -z "$line" ] && continue
    file=$(echo "$line" | awk '{print $2}')
    src_file="${BUILD_DIR}/${file}"
    if [ -f "${src_file}" ]; then
        cp "${src_file}" "${OUTPUT_DIR}/"
        echo "  Copied: $(basename "$file")"
    else
        echo "  Warning: file not found: ${src_file}"
    fi
done < <(tail -n +2 "${FLASH_ARGS_FILE}")

cp "${FLASH_ARGS_FILE}" "${OUTPUT_DIR}/flash_args.txt"

echo "Copying Windows esptool..."
if [ -f "${ESPTOOL_SOURCE}" ]; then
    mkdir -p "${OUTPUT_DIR}/${ESPTOOL_WIN_DIR}"
    cp "${ESPTOOL_SOURCE}" "${OUTPUT_DIR}/${ESPTOOL_WIN_DIR}/"
    echo "  Copied: esptool.exe"
fi

cat > "${OUTPUT_DIR}/README.txt" << 'README_EOF'
ESP32-S2 MINIBOX Production Firmware Pack

Files:
- flash.sh          Linux/Mac flash script
- flash.bat         Windows launcher
- flash_one.bat     Windows single-port flash with retry
- mac_addresses.txt Recorded MAC addresses (deduplicated, lowercase, no ':')
- flash_args.txt    Flash parameters reference
- mac_addresses.txt Recorded MAC addresses, deduplicated and stored without ':'
- *.bin             Firmware files

Usage:
Linux/Mac:
Linux/Mac:
  ./flash.sh
  ./flash.sh --read-mac
  ./flash.sh --read-mac /dev/ttyUSB0
  ./flash.sh /dev/ttyUSB1
  ./flash.sh /dev/ttyUSB0 /dev/ttyUSB1
  ./flash.sh /dev/ttyUSB*

Windows:
  flash.bat
  flash.bat --read-mac
  flash.bat --read-mac COM3
  flash.bat COM3
  flash.bat COM1 COM2 COM3
  flash.bat all
README_EOF

echo "Creating ZIP package..."
cd "${OUTPUT_DIR}"
zip -r "${ZIP_NAME}" . -x "${ZIP_NAME}"
mv "${ZIP_NAME}" "${BUILD_DIR}/"

echo "Pack complete!"
echo "Output dir: ${OUTPUT_DIR}"
echo "Package: ${BUILD_DIR}/${ZIP_NAME}"
