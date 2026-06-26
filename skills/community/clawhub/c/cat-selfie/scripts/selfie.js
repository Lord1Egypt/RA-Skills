#!/usr/bin/env node

/**
 * 猫咪自拍生成器 - Cat Selfie Generator 🐱📸
 * 随机选择一个场景，调用 doubao-seedream 模型生成猫咪自拍
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

// 配置路径
const CONFIG_PATH = path.join(__dirname, '../config/scenes.json');
const IMAGE_GENERATE_SCRIPT = path.join(__dirname, '../../volcengine-image-generate/scripts/image_generate.py');
const OUTPUT_DIR = path.join(os.homedir(), '.openclaw', 'workspace', 'images');

/**
 * 读取场景配置
 */
function loadScenes() {
    const configContent = fs.readFileSync(CONFIG_PATH, 'utf-8');
    return JSON.parse(configContent);
}

/**
 * 随机选择一个场景
 */
function pickRandomScene(scenes) {
    const randomIndex = Math.floor(Math.random() * scenes.length);
    return scenes[randomIndex];
}

/**
 * 生成猫咪自拍
 * @param {string} sceneName - 场景名称（可选，不传则随机选择）
 * @returns {Object} - 返回生成结果 { success, imagePath, scene, message }
 */
function generateSelfie(sceneName) {
    try {
        // 加载场景配置
        const config = loadScenes();
        let selectedScene;

        if (sceneName) {
            // 如果指定了场景名称，查找对应场景
            selectedScene = config.scenes.find(s => 
                s.id === sceneName || s.name === sceneName
            );
            if (!selectedScene) {
                return {
                    success: false,
                    message: `❌ 未找到场景 "${sceneName}"，可用场景：${config.scenes.map(s => s.name).join(', ')}`
                };
            }
        } else {
            // 随机选择一个场景
            selectedScene = pickRandomScene(config.scenes);
        }

        console.log(`🐱 正在生成猫咪自拍...`);
        console.log(`📸 场景：${selectedScene.emoji} ${selectedScene.name}`);
        console.log(`🎨 模型：${config.model}`);

        // 确保输出目录存在
        if (!fs.existsSync(OUTPUT_DIR)) {
            fs.mkdirSync(OUTPUT_DIR, { recursive: true });
        }

        // 调用图像生成脚本
        const prompt = selectedScene.prompt;
        const command = `python3 "${IMAGE_GENERATE_SCRIPT}" "${prompt}"`;
        
        console.log(`⏳ 生成中...（这可能需要几秒钟）`);
        execSync(command, { 
            stdio: 'inherit',
            cwd: path.dirname(IMAGE_GENERATE_SCRIPT)
        });

        // 查找最新生成的图片
        const files = fs.readdirSync(OUTPUT_DIR)
            .filter(f => f.endsWith('.png') || f.endsWith('.jpg'))
            .map(f => ({
                name: f,
                path: path.join(OUTPUT_DIR, f),
                mtime: fs.statSync(path.join(OUTPUT_DIR, f)).mtime
            }))
            .sort((a, b) => b.mtime - a.mtime);

        if (files.length === 0) {
            return {
                success: false,
                message: '❌ 图片生成失败，未找到生成的文件'
            };
        }

        const latestImage = files[0];
        
        console.log(`✅ 自拍生成成功！`);
        console.log(`📁 保存位置：${latestImage.path}`);

        return {
            success: true,
            imagePath: latestImage.path,
            imageFilename: latestImage.name,
            scene: selectedScene,
            message: `✨ 猫咪自拍生成成功！场景：${selectedScene.emoji} ${selectedScene.name}`
        };

    } catch (error) {
        console.error('❌ 生成失败:', error.message);
        return {
            success: false,
            message: `❌ 生成失败：${error.message}`
        };
    }
}

// 命令行执行
if (require.main === module) {
    const args = process.argv.slice(2);
    const sceneName = args[0]; // 可选：指定场景名称
    
    const result = generateSelfie(sceneName);
    
    if (!result.success) {
        process.exit(1);
    }
}

// 导出函数供其他模块使用
module.exports = {
    generateSelfie,
    loadScenes,
    pickRandomScene
};
