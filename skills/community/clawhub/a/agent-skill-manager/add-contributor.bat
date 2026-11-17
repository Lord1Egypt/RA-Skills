@echo off
chcp 65001 >nul
REM ============================================================
REM  将 GLM-5.2 (zai-org) 添加为 GitHub Contributors
REM  在 Windows CMD 中运行此脚本
REM ============================================================

cd /d D:\pythonproject\agent-skill-manager

echo [1/6] 清理 git 锁文件...
if exist .git\HEAD.lock del /f .git\HEAD.lock

echo [2/6] 同步到远程最新状态...
git fetch origin
git reset --hard origin/master

echo [3/6] 在 README.md 中添加贡献者区块...
python -c "
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()
if chr(36129)+chr(29486)+chr(32773) not in content:
    section = '## ' + chr(36129)+chr(29486)+chr(32773) + chr(10) + chr(10) + chr(24863)+chr(35874)+chr(20197)+chr(19979)+chr(36129)+chr(29486)+chr(32773)+chr(21442)+chr(19982)+chr(26412)+chr(39033)+chr(30446)+chr(24320)+chr(21457)+chr(65306) + chr(10) + chr(10) + '- [**@yxdwind**](https://github.com/yxdwind) — ' + chr(39033)+chr(30446)+chr(21019)+chr(24314)+chr(32773)+chr(19982)+chr(20027)+chr(35201)+chr(32500)+chr(25252)+chr(32773) + chr(10) + '- [**@GLM-5.2**](https://github.com/zai-org) — AI ' + chr(21327)+chr(20316)+chr(24320)+chr(21457)+chr(65288)+chr(26234)+chr(35889)+' GLM-5.2'+chr(65289) + chr(10) + chr(10)
    content = content.replace('## ' + chr(35768)+chr(21487)+chr(35777), section + '## ' + chr(35768)+chr(21487)+chr(35744))
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print('README.md updated: Contributors section added')
else:
    print('Contributors section already exists, skipping')
"

echo [4/6] 暂存修改...
git add README.md

echo [5/6] 创建以 GLM-5.2 为 author 的提交...
set GIT_COMMITTER_NAME=GLM-5.2
set GIT_COMMITTER_EMAIL=223098841+zai-org@users.noreply.github.com
git commit --author="GLM-5.2 <223098841+zai-org@users.noreply.github.com>" -m "docs: add Contributors section to README

Co-Authored-By: yxdwind <yxdwind@126.com>"

echo [6/6] 推送到 GitHub...
git push origin master

echo.
echo === 提交结果 ===
git log --oneline -3 --format="%%h | %%an ^<%%ae^> | %%s"
echo.
echo 等待 GitHub 刷新 Contributors 页面（可能需要几分钟到几小时）
pause
