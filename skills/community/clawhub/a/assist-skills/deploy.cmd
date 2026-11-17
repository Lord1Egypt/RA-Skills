@echo off
rem ============================================================
rem  assist-skills one-click deploy entry (Windows)
rem
rem  Usage:
rem    double-click              -> auto-detect the target project dir
rem                                 (vendored layout -> project root, else current dir,
rem                                  else it prompts)
rem    deploy.cmd D:\your-project
rem    deploy.cmd -Target D:\your-project -DryRun
rem    deploy.cmd -Shortcuts      -> also create SendTo / Desktop shortcuts
rem
rem  This file only locates the package and calls scripts\deploy.ps1.
rem  Parameters are identical to scripts\deploy.ps1:
rem    -Target <dir>  -Force  -DryRun  -SkipRules  -IncludeSkillFiles
rem
rem  NOTE: keep this file ASCII-only on purpose. Non-ASCII text in a .cmd
rem  file breaks cmd.exe line parsing under GBK code pages, so all Chinese
rem  messages are printed by scripts\deploy.ps1 instead.
rem ============================================================
setlocal EnableExtensions

set "SKILL_ROOT=%~dp0"
set "PS_SCRIPT=%SKILL_ROOT%scripts\deploy.ps1"

if not exist "%PS_SCRIPT%" goto :missing

rem Prefer PowerShell 7 (pwsh), fall back to Windows PowerShell.
set "PS_EXE=powershell"
where pwsh >nul 2>nul && set "PS_EXE=pwsh"

if "%~1"=="" goto :interactive

"%PS_EXE%" -NoProfile -File "%PS_SCRIPT%" %*
set "RC=%ERRORLEVEL%"
goto :report

:interactive
"%PS_EXE%" -NoProfile -File "%PS_SCRIPT%" -Auto
set "RC=%ERRORLEVEL%"
goto :report

:missing
echo [ERROR] deploy script not found: %PS_SCRIPT%
echo         deploy.cmd and the scripts\ folder must live in the same package.
set "RC=1"

:report
if "%RC%"=="0" goto :done
echo.
echo [HINT] Deploy finished with exit code %RC%.
echo        If the error is about execution policy ^(running scripts is disabled^),
echo        run the following once, then retry:
echo            Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

:done
echo.

rem Keep the window open when launched without arguments (double-click).
if "%~1"=="" pause

endlocal & exit /b %RC%
