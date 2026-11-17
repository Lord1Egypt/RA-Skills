@echo off
chcp 65001 >nul 2>nul
setlocal

rem =============================================================
rem  Disk cache cleaner - Windows launcher
rem  NOTE: this file must stay ASCII-only (no CJK chars).
rem        cmd reads .bat as GBK, CJK breaks parsing.
rem  Usage:
rem    double click              -> scan, then pick items to delete
rem    clean.bat --dry-run       -> scan only, delete nothing
rem    clean.bat --pick 1,3      -> delete item 1 and 3
rem    clean.bat --pick g        -> delete all "regenerable" items
rem    clean.bat --tier yellow   -> include "need re-download" items
rem =============================================================

set "PY="

rem 1) Python launcher (most reliable on Windows)
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 -c "import sys" >nul 2>nul
  if %errorlevel%==0 set "PY=py -3"
)

rem 2) python on PATH
if not defined PY (
  where python >nul 2>nul
  if %errorlevel%==0 set "PY=python"
)

rem 3) WorkBuddy managed python
if not defined PY (
  if exist "%USERPROFILE%\.workbuddy\binaries\python\versions\3.13.12\python.exe" (
    set "PY=%USERPROFILE%\.workbuddy\binaries\python\versions\3.13.12\python.exe"
  )
)

rem 4) Common install locations
if not defined PY (
  if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    set "PY=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
  )
)
if not defined PY (
  if exist "C:\Python313\python.exe" set "PY=C:\Python313\python.exe"
)

if not defined PY (
  echo [ERROR] Python not found. Install Python 3.8+ or add it to PATH.
  echo         https://www.python.org/downloads/
  echo.
  pause
  exit /b 1
)

%PY% "%~dp0clean_cache.py" %*

echo.
pause
