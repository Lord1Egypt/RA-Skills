@echo off
rem cad-file-reader Windows 专业识图入口（跨平台脚手架）：转发到 run_cad.py
python "%~dp0run_cad.py" cad_mep_geometry %*
