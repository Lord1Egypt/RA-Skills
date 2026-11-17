@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

REM ============================================================
REM  convert2docx.bat - 拖拽入口
REM  把一个或多个文件拖到本文件上即可批量转换
REM ============================================================

set "PS_SCRIPT=%~dp0convert2docx.ps1"

if "%~1"=="" (
    echo.
    echo ============================================
    echo   convert2docx - 文档转 Word
    echo ============================================
    echo.
    echo   用法：把一个或多个文件拖到本 bat 上
    echo.
    echo   支持格式：md / markdown / txt / html / htm
    echo             rtf / tex / rst / org / docx
    echo.
    echo   首次运行会要求配置 pandoc 和 reference.docx
    echo.
    pause
    exit /b 0
)

REM 用 C2D_FILES 环境变量传递文件列表（用 | 分隔，规避 PowerShell 参数绑定问题）
set "C2D_FILES="
:collect
if "%~1"=="" goto :run
set "C2D_FILES=!C2D_FILES!%~1|"
shift
goto :collect

:run
REM 去掉末尾的 |
if "!C2D_FILES:~-1!"=="|" set "C2D_FILES=!C2D_FILES:~0,-1!"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%PS_SCRIPT%"

echo.
pause
