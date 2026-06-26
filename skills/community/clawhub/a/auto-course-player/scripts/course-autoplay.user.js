// ==UserScript==
// @name         网课自动播放器 - 青岛大学继续教育学院
// @namespace    http://tampermonkey.net/
// @version      1.0.0
// @description  自动播放网课视频，静音播放，自动切换下一课
// @author       Bill (AI Assistant)
// @match        https://loginjxjyzx.qdu.edu.cn/*
// @match        https://studentjxjyzx.qdu.edu.cn/*
// @match        https://*.qdu.edu.cn/*
// @grant        none
// @run-at       document-end
// ==/UserScript==

(function() {
    'use strict';

    // ==================== 配置 ====================
    const CONFIG = {
        checkInterval: 10000,        // 检查间隔（毫秒）
        videoEndThreshold: 0.95,     // 视频完成阈值（95%）
        autoPlayDelay: 2000,         // 切换后延迟播放（毫秒）
        debugMode: false             // 调试模式
    };

    // ==================== 状态管理 ====================
    let state = {
        isRunning: false,
        currentVideo: null,
        completedVideos: [],
        startTime: null,
        checkTimer: null
    };

    // ==================== 工具函数 ====================
    function log(...args) {
        if (CONFIG.debugMode) {
            console.log('[CourseAutoplay]', ...args);
        }
    }

    function logInfo(...args) {
        console.info('[CourseAutoplay]', ...args);
    }

    function logError(...args) {
        console.error('[CourseAutoplay]', ...args);
    }

    // ==================== 核心功能 ====================

    /**
     * 获取当前视频元素
     */
    function getVideoElement() {
        return document.querySelector('video');
    }

    /**
     * 获取当前视频信息
     */
    function getCurrentVideoInfo() {
        const video = getVideoElement();
        if (!video) return null;

        const titleEl = document.querySelector('h1, h2, h3, [data-title], .video-title');
        const title = titleEl ? titleEl.textContent.trim() : '未知课程';

        return {
            title: title,
            currentTime: video.currentTime,
            duration: video.duration,
            progress: video.duration > 0 ? video.currentTime / video.duration : 0,
            isPlaying: !video.paused,
            isMuted: video.muted
        };
    }

    /**
     * 确保视频静音并播放
     */
    function ensurePlayingAndMuted() {
        const video = getVideoElement();
        if (!video) {
            log('未找到视频元素');
            return false;
        }

        let changed = false;

        // 确保静音
        if (!video.muted) {
            video.muted = true;
            video.volume = 0;
            changed = true;
            log('已静音');
        }

        // 确保播放
        if (video.paused) {
            video.play().then(() => {
                log('已开始播放');
            }).catch(err => {
                logError('播放失败:', err);
            });
            changed = true;
        }

        return changed;
    }

    /**
     * 查找下一个视频并点击
     */
    function clickNextVideo() {
        log('查找下一个视频...');

        // 在课程列表中查找下一个未完成的视频
        const courseList = document.querySelector('[role="tabpanel"]');
        if (!courseList) {
            logError('未找到课程列表');
            return false;
        }

        // 查找所有视频项
        const videoItems = courseList.querySelectorAll('[cursor="pointer"]');
        for (let item of videoItems) {
            const text = item.textContent;
            if (text.includes('视频') && !state.completedVideos.includes(text)) {
                log('找到下一个视频:', text);
                item.click();
                return true;
            }
        }

        log('未找到更多视频');
        return false;
    }

    /**
     * 处理弹窗
     */
    function handleDialog() {
        // 策略 1: 查找 dialog 角色元素中的确定按钮
        const dialog = document.querySelector('[role="dialog"]');
        if (dialog) {
            const confirmBtn = Array.from(dialog.querySelectorAll('[cursor="pointer"], button'))
                .find(btn => btn.textContent.includes('确定') || btn.textContent === 'OK');
            if (confirmBtn) {
                logInfo('检测到弹窗，自动关闭');
                confirmBtn.click();
                return true;
            }
        }

        // 策略 2: 查找包含"学习情况"、"学习时间"等关键词的弹窗
        const learningDialog = Array.from(document.querySelectorAll('[cursor="pointer"], button'))
            .find(btn => {
                const parent = btn.closest('[role="dialog"]') || btn.parentElement?.parentElement;
                if (parent) {
                    const text = parent.textContent;
                    return text.includes('学习情况') || text.includes('学习时间') || text.includes('学习时长');
                }
                return false;
            });

        if (learningDialog) {
            logInfo('检测到学习情况弹窗，自动关闭');
            // 查找同一个弹窗容器内的"确定"按钮
            const container = learningDialog.closest('[role="dialog"]') || learningDialog.parentElement?.parentElement;
            if (container) {
                const confirmBtn = Array.from(container.querySelectorAll('[cursor="pointer"], button'))
                    .find(btn => btn.textContent.includes('确定'));
                if (confirmBtn) {
                    confirmBtn.click();
                    return true;
                }
            }
        }

        // 策略 3: 通用 - 查找页面上任何"确定"按钮（作为最后手段）
        const confirmBtn = Array.from(document.querySelectorAll('[cursor="pointer"]'))
            .filter(btn => btn.textContent.trim() === '确定' || btn.textContent.trim() === '确定 ')
            .find(btn => {
                // 确保按钮在可见的弹窗内，而不是课程列表中
                const rect = btn.getBoundingClientRect();
                const isCentered = rect.top > window.innerHeight * 0.2 && rect.top < window.innerHeight * 0.8;
                return isCentered;
            });

        if (confirmBtn) {
            logInfo('检测到通用弹窗，自动关闭');
            confirmBtn.click();
            return true;
        }

        return false;
    }

    /**
     * 检查视频是否完成
     */
    function checkVideoCompleted() {
        const info = getCurrentVideoInfo();
        if (!info) return false;

        return info.progress >= CONFIG.videoEndThreshold;
    }

    /**
     * 切换到下一个视频
     */
    async function switchToNextVideo() {
        logInfo('开始切换下一课...');

        const info = getCurrentVideoInfo();
        if (info) {
            state.completedVideos.push(info.title);
            logInfo('已完成:', info.title);
        }

        // 点击下一个视频
        if (clickNextVideo()) {
            // 等待视频加载
            await new Promise(resolve => setTimeout(resolve, CONFIG.autoPlayDelay));

            // 处理弹窗
            handleDialog();

            // 确保播放和静音
            await new Promise(resolve => setTimeout(resolve, 500));
            ensurePlayingAndMuted();

            logInfo('切换完成');
            showNotification('已切换到下一课');
        }
    }

    // ==================== UI 控制 ====================

    /**
     * 创建控制面板
     */
    function createControlPanel() {
        // 检查是否已存在
        if (document.getElementById('course-autoplay-panel')) {
            return;
        }

        const panel = document.createElement('div');
        panel.id = 'course-autoplay-panel';
        panel.innerHTML = `
            <div style="
                position: fixed;
                top: 20px;
                right: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 15px;
                border-radius: 12px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                z-index: 999999;
                min-width: 200px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                color: white;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <h3 style="margin: 0; font-size: 16px;">🎓 网课自动播放</h3>
                    <button id="autoplay-close" style="
                        background: none;
                        border: none;
                        color: white;
                        font-size: 20px;
                        cursor: pointer;
                        padding: 0;
                        line-height: 1;
                    ">×</button>
                </div>
                <div style="margin-bottom: 10px;">
                    <div style="font-size: 12px; opacity: 0.8;">状态</div>
                    <div id="autoplay-status" style="font-size: 14px; font-weight: bold;">⏸️ 已暂停</div>
                </div>
                <div style="margin-bottom: 10px;">
                    <div style="font-size: 12px; opacity: 0.8;">已完成</div>
                    <div id="autoplay-count" style="font-size: 14px;">0 个视频</div>
                </div>
                <button id="autoplay-toggle" style="
                    width: 100%;
                    padding: 10px;
                    border: none;
                    border-radius: 8px;
                    background: white;
                    color: #667eea;
                    font-size: 14px;
                    font-weight: bold;
                    cursor: pointer;
                    transition: all 0.3s;
                ">▶️ 启动自动播放</button>
            </div>
        `;

        document.body.appendChild(panel);

        // 绑定事件
        document.getElementById('autoplay-toggle').addEventListener('click', toggleAutoplay);
        document.getElementById('autoplay-close').addEventListener('click', () => {
            panel.remove();
        });
    }

    /**
     * 更新面板状态
     */
    function updatePanel() {
        const statusEl = document.getElementById('autoplay-status');
        const countEl = document.getElementById('autoplay-count');
        const toggleBtn = document.getElementById('autoplay-toggle');

        if (!statusEl || !countEl || !toggleBtn) return;

        statusEl.textContent = state.isRunning ? '▶️ 运行中' : '⏸️ 已暂停';
        countEl.textContent = `${state.completedVideos.length} 个视频`;
        toggleBtn.textContent = state.isRunning ? '⏸️ 暂停' : '▶️ 启动自动播放';
        toggleBtn.style.background = state.isRunning ? '#ff6b6b' : 'white';
        toggleBtn.style.color = state.isRunning ? 'white' : '#667eea';
    }

    /**
     * 显示通知
     */
    function showNotification(message) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: #4caf50;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            z-index: 999999;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 14px;
            animation: slideIn 0.3s ease-out;
        `;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transition = 'opacity 0.3s';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    /**
     * 切换自动播放状态
     */
    function toggleAutoplay() {
        state.isRunning = !state.isRunning;

        if (state.isRunning) {
            logInfo('自动播放已启动');
            showNotification('🎉 自动播放已启动');
            state.startTime = Date.now();
            startMonitoring();
        } else {
            logInfo('自动播放已暂停');
            showNotification('⏸️ 自动播放已暂停');
            stopMonitoring();
        }

        updatePanel();
    }

    /**
     * 开始监控
     */
    function startMonitoring() {
        if (state.checkTimer) {
            clearInterval(state.checkTimer);
        }

        // 立即检查一次
        checkAndHandle();

        // 定期检查
        state.checkTimer = setInterval(checkAndHandle, CONFIG.checkInterval);
    }

    /**
     * 停止监控
     */
    function stopMonitoring() {
        if (state.checkTimer) {
            clearInterval(state.checkTimer);
            state.checkTimer = null;
        }
    }

    /**
     * 检查并处理
     */
    async function checkAndHandle() {
        if (!state.isRunning) return;

        // 优先处理弹窗（每次循环都检查）
        handleDialog();

        const video = getVideoElement();
        if (!video) {
            log('未找到视频，等待中...');
            return;
        }

        // 确保播放和静音
        ensurePlayingAndMuted();

        // 检查是否完成
        if (checkVideoCompleted()) {
            log('视频已完成，切换下一课...');
            await switchToNextVideo();
        }

        updatePanel();
    }

    // ==================== 初始化 ====================

    function init() {
        log('网课自动播放器已加载');

        // 延迟创建面板，确保页面已完全加载
        setTimeout(() => {
            createControlPanel();
            updatePanel();
            showNotification('🎓 网课自动播放器已就绪');
        }, 1000);
    }

    // 页面加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
