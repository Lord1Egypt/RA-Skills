@echo off
chcp 65001 >nul
title Douyin Favorites Progress
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0progress.ps1" %*
if errorlevel 1 (
  echo.
  echo progress.ps1 failed - press any key
  pause >nul
)
