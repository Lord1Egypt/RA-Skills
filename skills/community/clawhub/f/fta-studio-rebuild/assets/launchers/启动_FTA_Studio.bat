@echo off
setlocal
title FTA Studio

rem ============================================================
rem  FTA Studio - portable launcher
rem  Everything is relative to this folder. No install needed.
rem ============================================================

set "HERE=%~dp0"
if "%HERE:~-1%"=="\" set "HERE=%HERE:~0,-1%"
set "APPDIR=%HERE%\app"
set "NODEEXE=%HERE%\runtime\node.exe"

if not exist "%NODEEXE%" set "NODEEXE=node"

if not exist "%APPDIR%\src\launch.mjs" (
  echo.
  echo   [ERROR] Application files are missing.
  echo   Expected: %APPDIR%\src\launch.mjs
  echo.
  pause
  exit /b 1
)

echo.
echo   ============================================
echo     FTA Studio  -  Fault Tree Analysis
echo   ============================================
echo.
echo    Folder : %HERE%
echo    Node   : %NODEEXE%
echo.
echo    Starting in the background ...
echo.

powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "Start-Process -FilePath '%NODEEXE%' -ArgumentList 'src\launch.mjs' -WorkingDirectory '%APPDIR%' -WindowStyle Hidden"

ping -n 4 127.0.0.1 >nul

powershell -NoProfile -ExecutionPolicy Bypass -Command "try{ $c=New-Object Net.Sockets.TcpClient; $c.Connect('127.0.0.1',8777); $c.Close(); Write-Host '   OK : running at  http://localhost:8777/ ' }catch{ Write-Host '   NOTE : still starting, the browser will open by itself in a moment.' }"

echo.
echo    Browser :  http://localhost:8777/
echo    Backup  :  http://127.0.0.1:8777/
echo.
echo    The server keeps running after this window closes.
echo    To stop it, run the Stop script in this folder.
echo.
ping -n 4 127.0.0.1 >nul
