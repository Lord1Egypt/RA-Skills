@echo off
setlocal
title FTA Studio - stop

echo.
echo   Stopping FTA Studio ...
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command "$n=0; Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'node.exe' -and $_.CommandLine -match 'launch\.mjs' } | ForEach-Object { Write-Host ('  stopping pid ' + $_.ProcessId); Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue; $n++ }; if ( $n -eq 0 ) { Write-Host '  no running FTA Studio server was found' } else { Write-Host ('  stopped ' + $n + ' process(es)') }"

echo.
echo   Done. You can close this window.
echo.
ping -n 4 127.0.0.1 >nul
