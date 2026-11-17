@echo off
rem One command per check:  dnd-check.cmd --actor NAME --skill SKILL --dc 15
rem Runs dnd-check.py, which inserts the bundled engine into sys.path itself
rem (embedded Python builds ignore PYTHONPATH).
rem NOTE: keep this file ASCII-only - cmd.exe reads .cmd as ANSI.
setlocal
set "HERE=%~dp0"
set "PY=%HERE%dnd-engine\.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=%HERE%..\dnd-engine\.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
"%PY%" "%HERE%dnd-check.py" %*
exit /b %ERRORLEVEL%
