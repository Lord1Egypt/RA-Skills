@echo off
setlocal
title FTA Studio - install

echo.
echo   ============================================
echo     FTA Studio  -  install to this computer
echo   ============================================
echo.
echo   The tool will be copied to your user profile and
echo   a Desktop shortcut will be created.
echo.
echo   No administrator rights are required.
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1"

echo.
pause
