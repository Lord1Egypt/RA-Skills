@echo off
rem cad-file-reader Windows 依赖自检：复用 pyboot 的 vendor 检查（缺依赖会打印指引）。
python "%~dp0pyboot.py" %*
