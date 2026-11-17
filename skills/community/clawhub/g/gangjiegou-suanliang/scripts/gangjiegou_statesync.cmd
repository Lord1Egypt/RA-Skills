@echo off
rem gangjiegou_statesync launcher (ASCII only on purpose; untested on real Windows)
setlocal
set "HERE=%~dp0"
set "PY=%PYTHON%"
if not defined PY set "PY=%CODEX_PYTHON%"
if not defined PY set "PY=python"
"%PY%" "%HERE%gangjiegou_statesync.py" %*
