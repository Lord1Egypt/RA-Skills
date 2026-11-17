@echo off
rem awam-todo single entry: stop stale UI service, then start the UI backend
rem and the capture service (global hotkey -> clipboard -> triage) together.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start-awam-todo.ps1" %*
