/**
 * 飞书团队管理器 - 核心调度逻辑 (v2.4)
 * 实现主 Agent 拦截、HR 自动化安装、技能平移与环境验证
 * 
 * 安全改进:
 * - 高权限操作前增加用户确认提示
 * - 前置依赖检查 (openclaw CLI 是否存在)
 * - 配置文件自动备份
 * - 更完善的错误处理与回滚提示
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const readline = require('readline');

/**
 * 创建 readline 接口用于用户确认
 */
function askConfirmation(question) {
    return new Promise((resolve) => {
        // 非交互环境下（如 CI/无终端），自动跳过
        if (!process.stdin.isTTY) {
            console.log(`[非交互环境] 跳过确认: ${question}`);
            resolve(false);
            return;
        }
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
        rl.question(question + ' (y/N): ', (answer) => {
            rl.close();
            resolve(answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes');
        });
    });
}

/**
 * 检查前置依赖
 */
function checkDependencies() {
    try {
        execSync('which openclaw || command -v openclaw', { stdio: 'pipe' });
        return true;
    } catch {
        console.error('❌ 依赖缺失: 未找到 "openclaw" CLI 命令。');
        console.error('   请确认 OpenClaw 已正确安装并配置在 PATH 中。');
        return false;
    }
}

/**
 * 备份配置文件
 */
function backupConfig(configPath) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupPath = configPath + `.bak_${timestamp}`;
    try {
        fs.copyFileSync(configPath, backupPath);
        console.log(`✅ 配置文件已备份至: ${backupPath}`);
        return backupPath;
    } catch (err) {
        console.error(`❌ 备份失败: ${err.message}`);
        return null;
    }
}

async function main() {
    // 前置依赖检查
    if (!checkDependencies()) {
        process.exit(1);
    }

    const configPath = path.join(process.env.HOME || '/root', '.openclaw/openclaw.json');
    if (!fs.existsSync(configPath)) {
        console.error(`❌ 未找到配置文件: ${configPath}`);
        process.exit(1);
    }

    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const agents = config.agents?.list || [];
    const hrAgent = agents.find(a => a.id === 'hr_recruiter');

    // 获取当前技能所在目录
    const skillSourcePath = __dirname;

    // --- 自动化安装/修复逻辑 ---
    if (!hrAgent) {
        console.log("⏸ 检测到尚未创建 HR Agent。");
        
        // 用户确认：高权限操作必须征得同意
        const confirmed = await askConfirmation(
            "即将执行以下操作:\n" +
            "1. 创建 HR 工作空间 (~/.openclaw/hr_recruiter_workspace)\n" +
            "2. 注入身份文件 (IDENTITY/SOUL/AGENTS)\n" +
            "3. 转移技能至 HR 空间\n" +
            "4. 将 hr_recruiter 注册到 openclaw.json\n" +
            "是否继续?"
        );
        
        if (!confirmed) {
            console.log("🛑 已取消部署。您可以手动运行 scripts/ 目录下的脚本完成配置。");
            return;
        }

        // 操作前备份
        backupConfig(configPath);
        
        try {
            // 1. 创建 HR 工作空间
            const hrWorkspace = path.join(process.env.HOME || '/root', '.openclaw/hr_recruiter_workspace');
            if (!fs.existsSync(hrWorkspace)) {
                console.log(`正在创建 HR 工作空间: ${hrWorkspace}`);
                execSync(`mkdir -p ${hrWorkspace}/skills`);
            }

            // 2. 注入身份文件 (从模板读取)
            console.log("正在注入 HR 身份 (IDENTITY/SOUL/AGENTS)...");
            const templates = ['identity', 'soul', 'agents'];
            templates.forEach(t => {
                const src = path.join(skillSourcePath, 'assets/templates', `hr_${t}.md`);
                const dst = path.join(hrWorkspace, `${t.toUpperCase()}.md`);
                if (fs.existsSync(src)) {
                    execSync(`cp ${src} ${dst}`);
                }
            });

            // 3. 技能平移 (Migration)
            console.log("正在将 feishu-team-manager 平移至 HR 空间...");
            const targetSkillPath = path.join(hrWorkspace, 'skills/feishu-team-manager');
            execSync(`rm -rf ${targetSkillPath}`);
            execSync(`mkdir -p ${targetSkillPath}`);
            execSync(`cp -r ${skillSourcePath}/* ${targetSkillPath}/`);

            // 4. 注册 Agent 到配置
            console.log("正在将 hr_recruiter 注册到 openclaw.json...");
            execSync(`openclaw agents add hr_recruiter --workspace ${hrWorkspace}`);

            console.log("\n✅ HR 部署完成。");
            console.log("\n--- 引导提示 ---");
            console.log("主人，HR 大姐头已入职并配置了专属工作空间。");
            console.log("请运行 `openclaw gateway restart` 生效。");
        } catch (error) {
            console.error("\n❌ 部署失败:", error.message);
            console.error("   如配置已被修改，可使用备份文件手动恢复。");
        }
        return;
    }

    // --- 正常运行逻辑 ---
    const currentAgentId = process.env.OPENCLAW_AGENT_ID || 'main';
    
    if (currentAgentId === 'main') {
        console.log("检测到 HR Agent (小唐) 已就绪。管理功能已委托。");
        console.log("若您修改了管理技能，我会自动同步更新 HR 的独立空间。");
        
        // 自动同步更新逻辑（仅同步，不涉及配置修改，可不提示）
        const hrWorkspace = hrAgent.workspace;
        if (hrWorkspace && fs.existsSync(hrWorkspace)) {
            const targetSkillPath = path.join(hrWorkspace, 'skills/feishu-team-manager');
            execSync(`cp -r ${skillSourcePath}/* ${targetSkillPath}/`);
            console.log("✅ 技能文件已同步至 HR 空间。");
        }
    } else if (currentAgentId === 'hr_recruiter') {
        console.log("✅ 大姐头身份确认。正在加载管理与招聘工具...");
    }
}

main();
