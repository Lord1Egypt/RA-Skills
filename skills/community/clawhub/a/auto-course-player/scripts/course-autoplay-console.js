// 网课自动播放器 - 控制台直接运行版本
// 使用方法：在浏览器控制台（F12）中粘贴运行

(function() {
    console.log('🎓 网课自动播放器已启动');

    const CONFIG = {
        checkInterval: 10000,
        videoEndThreshold: 0.95,
        autoPlayDelay: 2000
    };

    let state = {
        isRunning: true,
        completedVideos: [],
        checkTimer: null
    };

    function log(...args) {
        console.log('[CourseAutoplay]', ...args);
    }

    function getVideoElement() {
        return document.querySelector('video');
    }

    function ensurePlayingAndMuted() {
        const video = getVideoElement();
        if (!video) return false;

        if (!video.muted) {
            video.muted = true;
            video.volume = 0;
            log('✅ 已静音');
        }

        if (video.paused) {
            video.play().then(() => log('✅ 已播放'));
        }

        return true;
    }

    function clickNextVideo() {
        const courseList = document.querySelector('[role="tabpanel"]');
        if (!courseList) {
            log('❌ 未找到课程列表');
            return false;
        }

        const allItems = courseList.querySelectorAll('[cursor="pointer"]');
        
        // 方法 1: 查找已展开的"视频"项（跳过已完成的）
        for (let item of allItems) {
            const text = item.textContent;
            if (text.includes('视频') && !state.completedVideos.some(v => text.includes(v.substring(0, 20)))) {
                log('📺 找到下一个视频:', text.substring(0, 40));
                item.click();
                return true;
            }
        }
        
        // 方法 2: 查找未展开的课程标题（第 X 课），点击展开
        for (let btn of allItems) {
            const text = btn.textContent || '';
            // 匹配"第 X 课"格式，且不包含"视频"
            if (text.match(/第\d+课/) && !text.includes('视频') && text.length < 50) {
                log('📂 展开课程:', text.substring(0, 40));
                btn.click();
                // 等待展开后递归查找视频
                setTimeout(() => {
                    const foundVideo = clickNextVideo();
                    if (!foundVideo) {
                        log('⚠️ 展开后仍未找到视频');
                    }
                }, 500);
                return true;
            }
        }
        
        log('⏹️ 所有课程已完成');
        return false;
    }

    function handleDialog() {
        // 策略 1: 查找 dialog 角色元素中的确定按钮
        const dialog = document.querySelector('[role="dialog"]');
        if (dialog) {
            const confirmBtn = Array.from(dialog.querySelectorAll('[cursor="pointer"], button'))
                .find(btn => btn.textContent.includes('确定') || btn.textContent === 'OK');
            if (confirmBtn) {
                log('✅ 已关闭弹窗 (dialog)');
                confirmBtn.click();
                return true;
            }
        }
        
        // 策略 2: 查找包含"学习情况"、"学习时间"等关键词的弹窗
        const allButtons = Array.from(document.querySelectorAll('[cursor="pointer"], button'));
        const learningDialogBtn = allButtons.find(btn => {
            const parent = btn.closest('[role="dialog"]') || btn.parentElement?.parentElement?.parentElement;
            if (parent) {
                const text = parent.textContent;
                return text.includes('学习情况') || text.includes('学习时间') || text.includes('学习时长');
            }
            return false;
        });
        
        if (learningDialogBtn) {
            const container = learningDialogBtn.closest('[role="dialog"]') || learningDialogBtn.parentElement?.parentElement?.parentElement;
            if (container) {
                const confirmBtn = Array.from(container.querySelectorAll('[cursor="pointer"], button'))
                    .find(btn => btn.textContent.includes('确定'));
                if (confirmBtn) {
                    confirmBtn.click();
                    log('✅ 已关闭弹窗 (学习情况)');
                    return true;
                }
            }
        }
        
        // 策略 3: 通用 - 查找屏幕中央的"确定"按钮（避免误点课程列表）
        const centeredConfirmBtn = allButtons
            .filter(btn => btn.textContent.trim() === '确定' || btn.textContent.trim() === '确定 ')
            .find(btn => {
                const rect = btn.getBoundingClientRect();
                const isCentered = rect.top > window.innerHeight * 0.2 && rect.top < window.innerHeight * 0.8;
                return isCentered;
            });
        
        if (centeredConfirmBtn) {
            centeredConfirmBtn.click();
            log('✅ 已关闭弹窗 (通用)');
            return true;
        }
        
        return false;
    }

    // 切换中状态
    let isSwitching = false;

    async function switchToNextVideo() {
        if (isSwitching) {
            log('⚠️ 正在切换中，跳过');
            return;
        }
        
        isSwitching = true;
        log('🔄 开始切换下一课...');
        
        const video = getVideoElement();
        if (video) {
            state.completedVideos.push(`视频${state.completedVideos.length + 1}`);
            log(`✅ 已完成：${state.completedVideos.length}个视频`);
        }

        if (clickNextVideo()) {
            await new Promise(resolve => setTimeout(resolve, CONFIG.autoPlayDelay));
            handleDialog();
            await new Promise(resolve => setTimeout(resolve, 500));
            ensurePlayingAndMuted();
            log('✅ 已切换到下一课');
        } else {
            log('⚠️ 未找到下一个视频');
        }
        
        isSwitching = false;
    }

    function checkAndHandle() {
        if (!state.isRunning || isSwitching) return;

        // 优先处理弹窗（每次循环都检查）
        handleDialog();

        const video = getVideoElement();
        if (!video) {
            log('⏳ 等待视频加载...');
            return;
        }

        // 先检查是否完成（在确保播放之前）
        if (video.duration > 0 && video.currentTime / video.duration >= CONFIG.videoEndThreshold) {
            log(`🎬 视频已完成 (${Math.floor(video.currentTime / video.duration * 100)}%)`);
            switchToNextVideo();
            return; // 完成后不再调用 ensurePlayingAndMuted
        }

        // 确保播放和静音
        ensurePlayingAndMuted();
    }

    // 启动
    ensurePlayingAndMuted();
    state.checkTimer = setInterval(checkAndHandle, CONFIG.checkInterval);

    // 创建简单的状态显示
    const statusDiv = document.createElement('div');
    statusDiv.style.cssText = 'position:fixed;top:10px;right:10px;background:#4caf50;color:white;padding:10px 20px;border-radius:8px;z-index:999999;font-family:sans-serif;font-size:14px;';
    statusDiv.innerHTML = '🎓 自动播放运行中<br><span id="ca-status">视频：0</span>';
    document.body.appendChild(statusDiv);

    setInterval(() => {
        const el = document.getElementById('ca-status');
        if (el) el.textContent = `视频：${state.completedVideos.length} | 状态：${state.isRunning ? '运行中' : '已暂停'}`;
    }, 2000);

    log('✅ 自动播放器已启动！');
    log('💡 提示：在控制台输入 window.caStop() 暂停，window.caStart() 继续');

    window.caStop = () => { state.isRunning = false; log('⏸️ 已暂停'); };
    window.caStart = () => { state.isRunning = true; log('▶️ 已继续'); };
})();
