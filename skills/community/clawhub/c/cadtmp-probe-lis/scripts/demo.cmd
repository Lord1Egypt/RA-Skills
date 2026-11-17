@echo off
rem cad-file-reader Windows 简明演示：先跑内置样例扫描（完整演示见 demo.sh）。
python "%~dp0run_cad.py" cad_scan ".\examples\sample_room.dxf" --only 墙,柱 --format json --concise %*
