@echo off
rem cad-file-reader -> lis-skill-bus optional wiring (thin wrapper). Windows 兼容启动器。
setlocal EnableExtensions
set PY=python
where py >nul 2>nul
if not errorlevel 1 set PY=py
if not "%PYTHON%"=="" set PY=%PYTHON%
if not "%CODEX_PYTHON%"=="" set PY=%CODEX_PYTHON%
"%PY%" "%~dp0cad_statesync.py" %*
exit /b %errorlevel%
