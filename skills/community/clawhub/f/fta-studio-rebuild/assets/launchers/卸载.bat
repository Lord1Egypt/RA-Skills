@echo off
setlocal
title FTA Studio - uninstall

echo.
echo   This will remove FTA Studio from this computer:
echo     - the installed folder in your user profile
echo     - the Desktop shortcut
echo     - the Start Menu entry
echo.
echo   (Your fault-tree data is kept in the browser, it is not touched.)
echo.

set /p CONFIRM=  Type Y to continue:
if /i not "%CONFIRM%"=="Y" (
  echo.
  echo   Cancelled.
  ping -n 3 127.0.0.1 >nul
  exit /b 0
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0uninstall.ps1"

echo.
pause
