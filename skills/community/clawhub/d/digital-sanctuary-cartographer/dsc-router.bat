@echo off
:: DSC Command Router
:: Handles: /map-sanctuary, /stress-test, /export-atlas

set "COMMAND=%~1"

if /i "%COMMAND%"=="map-sanctuary" (
    call scripts\map-sanctuary.bat
) else if /i "%COMMAND%"=="stress-test" (
    call scripts\stress-test.bat
) else if /i "%COMMAND%"=="export-atlas" (
    call scripts\export-atlas.bat
) else (
    echo [DSC] Unknown command: %COMMAND%
    echo.
    echo Available commands:
    echo   /map-sanctuary   - Generate sanctuary map
    echo   /stress-test     - Run boundary stress tests
    echo   /export-atlas    - Export atlas as JSON capsule
)