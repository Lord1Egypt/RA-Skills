// 全局状态
const state = {
    darkMode: false,
    showEditor: true,
    works: [],
    allWorks: [], // 用于搜索
    selectedWork: null,
    hasApiKey: false,
    hasModelApiKey: false,
    config: null,
    selectedModel: 0,
    selectedSize: 0,
    selectedQuality: 1,
    selectedCut: 1,
    uploadedImages: [],
    currentLang: 'zh',
    i18n: null,
    searchKeyword: '',
    // 分页状态
    currentPage: 1,
    totalPages: 1,
    total: 0
};

// 常量
const MAX_IMAGES = 6;

// 语言简称映射
const langShortNames = {
    'zh': '中',
    'en': 'EN',
    'zh-TW': '繁',
    'ja': '日'
};

// DOM 元素
const elements = {
    gallery: document.getElementById('gallery'),
    editor: document.getElementById('editor'),
    editorInput: document.getElementById('editor-input'),
    editorUpload: document.getElementById('editor-upload'),
    uploadBtn: document.getElementById('upload-btn'),
    fileInput: document.getElementById('file-input'),
    submitBtn: document.getElementById('submit-btn'),
    viewer: document.getElementById('viewer'),
    viewerImage: document.getElementById('viewer-image'),
    viewerCuts: document.getElementById('viewer-cuts'),
    langMenu: document.getElementById('lang-menu'),
    searchInput: document.getElementById('search-input')
};

// 初始化
async function init() {
    // 加载语言
    await loadLanguage();
    
    // 加载主题状态
    loadThemeState();
    
    // 加载配置
    loadConfigFromLocalStorage();
    
    // 发送配置到后端
    await sendConfigToBackend();
    
    // 加载作品
    await loadWorks();
    
    // 设置事件监听
    setupEventListeners();
    
    // 设置滚动加载
    setupScrollLoad();
    
    // 加载参数
    await loadParameters();
    
    // 更新语言按钮显示
    updateLangButton();
    
    // 恢复未提交的提示词
    restorePendingPrompt();
    
    // 自动获取待处理任务
    await autoFetchPendingTasks();
    
    // 如果有待轮询的任务，启动轮询
    if (pollingTasks.size > 0) {
        startPolling();
    }
}

// 恢复未提交的提示词
function restorePendingPrompt() {
    const pendingPrompt = localStorage.getItem('banana_pending_prompt');
    if (pendingPrompt) {
        elements.editorInput.textContent = pendingPrompt;
    }
}

// 保存提示词到localStorage
function savePendingPrompt() {
    const prompt = elements.editorInput.textContent.trim();
    if (prompt) {
        localStorage.setItem('banana_pending_prompt', prompt);
    }
    // 空提示词不保存，也不清除（保留之前的）
}

// 清除提示词
function clearPendingPrompt() {
    localStorage.removeItem('banana_pending_prompt');
}

// 自动获取待处理任务
async function autoFetchPendingTasks() {
    const pendingWorks = state.works.filter(w => w.state === 1 || w.state === 99);
    
    if (pendingWorks.length === 0) return;
    
    // 批量提交获取请求
    const fetchPromises = pendingWorks.map(work => fetchTaskStatus(work.id));
    
    // 并行获取所有任务
    await Promise.all(fetchPromises);
}

// 获取单个任务状态
async function fetchTaskStatus(id) {
    try {
        const apiKey = localStorage.getItem('banana_api_key') || '';
        const response = await fetch(`/api/poll/${id}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ api_key: apiKey })
        });
        const result = await response.json();
        
        if (result.success && result.status === 'completed') {
            showToast('success', `任务 ${id} 获取成功！`);
            // 更新单个任务数据
            const workIndex = state.works.findIndex(w => w.id === id);
            if (workIndex !== -1 && result.data) {
                state.works[workIndex] = {
                    ...state.works[workIndex],
                    state: 10,
                    path: result.data.path,
                    response_data: result.data.response_data
                };
                // 立即更新该任务的图片展示
                renderGallery();
            }
        } else if (result.success && result.status === 'pending') {
            // 任务还在处理中，加入轮询队列
            pollingTasks.add(id);
        }
    } catch (error) {
        console.error(`任务 ${id} 获取失败:`, error);
    }
}

// 轮询任务集合
let pollingTasks = new Set();
let pollingInterval = null;

// 开始轮询
function startPolling() {
    if (pollingInterval) return;
    
    console.log('🔄 启动前端轮询，间隔 20 秒');
    
    const apiKey = localStorage.getItem('banana_api_key') || '';
    
    pollingInterval = setInterval(async () => {
        if (pollingTasks.size === 0) {
            stopPolling();
            return;
        }
        
        console.log(`🔄 轮询中，待处理任务: ${pollingTasks.size} 个`);
        
        const taskIds = Array.from(pollingTasks);
        for (const id of taskIds) {
            try {
                const response = await fetch(`/api/poll/${id}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ api_key: apiKey })
                });
                const result = await response.json();
                
                if (result.success && result.status === 'completed') {
                    pollingTasks.delete(id);
                    showToast('success', `任务 ${id} 获取成功！`);
                    
                    // 更新数据
                    const workIndex = state.works.findIndex(w => w.id === id);
                    if (workIndex !== -1 && result.data) {
                        state.works[workIndex] = {
                            ...state.works[workIndex],
                            state: 10,
                            path: result.data.path,
                            response_data: result.data.response_data
                        };
                    }
                    renderGallery();
                } else if (result.success && result.status === 'failed') {
                    pollingTasks.delete(id);
                    showToast('error', `任务 ${id} 失败: ${result.msg || '未知错误'}`);
                    // 更新状态为失败
                    const workIndex = state.works.findIndex(w => w.id === id);
                    if (workIndex !== -1) {
                        state.works[workIndex].state = 99;
                        state.works[workIndex].error = result.msg;
                    }
                    renderGallery();
                }
            } catch (error) {
                console.error(`轮询任务 ${id} 失败:`, error);
            }
        }
    }, 20000); // 每20秒轮询一次
}

// 停止轮询
function stopPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
    }
}

// 加载语言
async function loadLanguage() {
    let savedLang = localStorage.getItem('banana_lang');
    
    if (!savedLang) {
        const systemLang = navigator.language || navigator.userLanguage;
        if (systemLang.startsWith('zh-TW') || systemLang.startsWith('zh-HK')) {
            savedLang = 'zh-TW';
        } else if (systemLang.startsWith('zh')) {
            savedLang = 'zh';
        } else if (systemLang.startsWith('ja')) {
            savedLang = 'ja';
        } else {
            savedLang = 'en';
        }
    }
    
    state.currentLang = savedLang;
    
    try {
        const response = await fetch(`/lan/${savedLang}.json`);
        if (response.ok) {
            state.i18n = await response.json();
            applyTranslations();
        }
    } catch (error) {
        console.error('加载语言文件失败:', error);
    }
}

// 应用翻译
function applyTranslations() {
    if (!state.i18n) return;
    
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const text = getNestedValue(state.i18n, key);
        if (text) el.textContent = text;
    });
    
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        const text = getNestedValue(state.i18n, key);
        if (text) {
            el.placeholder = text;
            el.setAttribute('data-placeholder', text);
        }
    });
    
    // 更新编辑器输入框的 placeholder
    const placeholder = getNestedValue(state.i18n, 'editor.placeholder');
    if (placeholder) {
        elements.editorInput.setAttribute('data-placeholder', placeholder);
    }
}

// 获取嵌套对象的值
function getNestedValue(obj, path) {
    return path.split('.').reduce((acc, part) => acc && acc[part], obj);
}

// 获取翻译文本
function t(key) {
    return getNestedValue(state.i18n, key) || key;
}

// 更新语言按钮显示
function updateLangButton() {
    const langText = document.getElementById('lang-text');
    if (langText && state.config && state.config.languages) {
        const lang = state.config.languages.find(l => l.code === state.currentLang);
        langText.textContent = lang ? lang.short : '中';
    }
}

// 切换语言
function switchLanguage(lang) {
    localStorage.setItem('banana_lang', lang);
    // 刷新页面
    window.location.reload();
}

// 加载主题状态
function loadThemeState() {
    const savedTheme = localStorage.getItem('banana_dark_mode');
    if (savedTheme !== null) {
        state.darkMode = savedTheme === 'true';
        document.body.classList.toggle('dark', state.darkMode);
        updateThemeIcon();
    }
}

// 更新主题图标
function updateThemeIcon() {
    const sunIcon = document.querySelector('.sun-icon');
    const moonIcon = document.querySelector('.moon-icon');
    if (sunIcon && moonIcon) {
        sunIcon.style.display = state.darkMode ? 'none' : 'block';
        moonIcon.style.display = state.darkMode ? 'block' : 'none';
    }
}

// 保存主题状态
function saveThemeState() {
    localStorage.setItem('banana_dark_mode', state.darkMode.toString());
}

// 从 localStorage 加载配置
function loadConfigFromLocalStorage() {
    const apiKey = localStorage.getItem('banana_api_key') || '';
    const platformToken = localStorage.getItem('banana_platform_token') || '';
    const modelApiKey = localStorage.getItem('banana_model_api_key') || '';
    const savePath = localStorage.getItem('banana_save_path') || '';
    
    state.hasApiKey = !!apiKey;
    state.hasModelApiKey = !!modelApiKey;
    
    const savedModel = localStorage.getItem('banana_selected_model');
    const savedSize = localStorage.getItem('banana_selected_size');
    const savedQuality = localStorage.getItem('banana_selected_quality');
    const savedCut = localStorage.getItem('banana_selected_cut');
    
    if (savedModel !== null) state.selectedModel = parseInt(savedModel);
    if (savedSize !== null) state.selectedSize = parseInt(savedSize);
    if (savedQuality !== null) state.selectedQuality = parseInt(savedQuality);
    if (savedCut !== null) state.selectedCut = parseInt(savedCut);
}

// 发送配置到后端
async function sendConfigToBackend() {
    const apiKey = localStorage.getItem('banana_api_key') || '';
    
    if (!apiKey) {
        showSettings();
        return;
    }
    
    // 配置通过创作/轮询时传输，不再单独保存
}

// 显示设置弹窗
function showSettings() {
    win('settings', '设置', 'settings.html', 520, 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)');
}

// 显示AI提示词弹窗
function showPromptModal() {
    win('ai-prompt', 'AI提示词工具 - 创建多图片prompt', 'ai-prompt.html', 700, 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)');
}

// 显示错误弹窗
function showErrorModal(errorMsg) {
    window._winErrorMsg = errorMsg;
    win('error', '错误信息', 'error.html', 500, '#fee2e2');
}

// 显示关于弹窗
function showAboutModal() {
    win('about', '关于', 'about.html', 450, '');
}

// 加载作品列表
async function loadWorks(page = 1, append = false, keyword = '') {
    try {
        const pageSize = 30;
        let url = `/api/works?page=${page}&pageSize=${pageSize}`;
        if (keyword) {
            url += `&keyword=${encodeURIComponent(keyword)}`;
        }
        const response = await fetch(url);
        const data = await response.json();
        if (data.success) {
            if (append) {
                state.works = [...state.works, ...data.data];
            } else {
                state.works = data.data;
            }
            state.allWorks = state.works;
            state.currentPage = data.pagination.page;
            state.totalPages = data.pagination.totalPages;
            state.total = data.pagination.total;
            state.searchKeyword = keyword;
            renderGallery();
            
            // 加载成功，允许下次加载
            if (data.data.length > 0) {
                window.can_load = 1;
            }
        }
    } catch (error) {
        console.error('加载作品失败:', error);
    }
}

// 加载更多
async function loadMoreWorks() {
    if (state.currentPage < state.totalPages) {
        await loadWorks(state.currentPage + 1, true, state.searchKeyword);
    }
}

// 搜索作品 - 从数据库查询
async function searchWorks(keyword) {
    const trimmedKeyword = keyword.trim();
    window.can_load = 1; // 搜索时重置加载标志
    await loadWorks(1, false, trimmedKeyword);
}

// 渲染瀑布流
function renderGallery() {
    const validWorks = state.works.filter(w => w.state !== -1);
    
    if (validWorks.length === 0) {
        elements.gallery.innerHTML = `<div style="width:100%;display:flex;max-width: 1600px;margin: 0 auto;float:left;position:absolute;justify-content:center">
            <div style="grid-column: 1/-1; text-align: center; padding: 60px; opacity: 0.8;">
                <div style="font-size: 48px; margin-bottom: 16px;">🎨</div>
                <div style="font-size: 18px; margin-bottom: 8px;">${state.searchKeyword ? t('messages.noResults') : t('messages.noWorks')}</div>
                <div style="font-size: 14px;">${t('messages.startCreate')}</div>
            </div>
            </div>
        `;
        return;
    }

    elements.gallery.innerHTML = validWorks.map(work => {
        const date = new Date(work.date);
        const dateStr = `${date.getMonth()+1}-${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`;
        
        // 获取比例类名
        const ratioClass = work.ratio ? `ratio-${work.ratio.replace(':', '-')}` : 'ratio-1-1';
        
        // 构建底部信息
        const infoItems = [];
        infoItems.push(work.ratio || '1:1');
        infoItems.push(work.quality || '2K');
        if (work.cut > 1) infoItems.push(`${work.cut}宫格`);
        const infoText = infoItems.join(' · ');
        
        // 处理中或失败的任务
        if (work.state === 1 || work.state === 99) {
            const statusClass = work.state === 1 ? 'status-pending' : 'status-failed';
            const statusText = work.state === 1 ? '正在生成中' : '生成失败';
            const icon = work.state === 1 ? 
                `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>` :
                `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`;
            
            return `
                <div class="image-card task-card ${statusClass} ${ratioClass}" onclick="showTaskDetail(${work.id})">
                    <div class="task-status">
                        <div class="task-status-icon">${icon}</div>
                        <div class="task-status-text">${statusText}</div>
                    </div>
                    <div class="info">
                        <div class="prompt" onclick="event.stopPropagation(); showTaskDetail(${work.id})">${work.prompt}</div>
                        <div class="meta">
                            <span>${infoText}</span>
                            <span class="date">${dateStr}</span>
                        </div>
                    </div>
                    ${work.state === 99 ? `<button class="card-delete-btn" onclick="event.stopPropagation(); deleteTask(${work.id})">🗑️</button>` : ''}
                </div>
            `;
        }
        
        // 已完成的任务
        let httpPath = work.http_path;
        if (!httpPath && work.path) {
            // 兼容旧数据，尝试转换路径
            httpPath = work.path.replace(/^[A-Z]:\\Users\\[^\\]+\\Desktop\\banana2/i, '/images');
        }
        const imgSrc = `${httpPath}/thumb.png`;
        const mainSrc = `${httpPath}/main.png`;
        
        return `
            <div class="image-card ${ratioClass}" onclick="viewWork(${work.id})" onerror="handleImageError(${work.id}, this)">
                <img src="${imgSrc}" alt="${work.prompt}" onerror="this.onerror=null; this.src='${mainSrc}'; if(this.naturalWidth===0){this.parentElement.classList.add('image-error'); this.style.display='none';}">
                <div class="info">
                    <div class="prompt" onclick="event.stopPropagation(); showTaskDetail(${work.id})">${work.prompt}</div>
                    <div class="meta">
                        <span>${infoText}</span>
                        <span class="date">${dateStr}</span>
                        <button class="folder-btn" onclick="event.stopPropagation(); openFolder(${work.id})" title="打开文件夹">📁</button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    // 滚动加载更多（移除按钮，改用滚动检测）
}

// 滚动加载检测
window.can_load = 1;

function setupScrollLoad() {
    $('main').on('scroll', function() {
        // 检查是否滚动到底部300px
        if ($(this).scrollTop() + $(this).innerHeight() >= this.scrollHeight - 300) {
            if (window.can_load == 1 && state.currentPage < state.totalPages) {
                window.can_load = 0;
                loadMoreWorks();
            }
        }
    });
}

// 图片加载失败处理
function handleImageError(id, element) {
    element.classList.add('image-error');
}

// 打开文件夹
function openFolder(workId) {
    const work = state.works.find(w => w.id === workId);
    if (!work || !work.path) {
        showToast('error', '找不到任务路径');
        return;
    }
    
    $.ajax({
        url: '/api/open-folder',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ path: work.path })
    });
}

// 显示任务详情弹窗
function showTaskDetail(id) {
    // 保存任务ID到全局变量，供组件使用
    window._winTaskId = id;
    win('task-detail', '任务详情', 'task-detail.html', 450, 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)');
}

// 复制到剪贴板
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('success', '已复制到剪贴板');
    }).catch(() => {
        showToast('error', '复制失败');
    });
}

// 获取图片 - 只查询task状态
async function retryTask(id) {
    const work = state.works.find(w => w.id === id);
    if (!work) return;
    
    // 不关闭弹窗
    const btn = document.querySelector('.task-btn-retry');
    const originalText = btn.textContent;
    btn.textContent = '获取中...';
    btn.disabled = true;
    
    try {
        const apiKey = localStorage.getItem('banana_api_key') || '';
        const response = await fetch(`/api/poll/${id}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ api_key: apiKey })
        });
        const result = await response.json();
        
        // 显示Toast通知
        if (result.success) {
            if (result.status === 'completed') {
                showToast('success', '获取成功！图片已保存');
                closeTaskDetail();
                // 更新单个任务数据
                const workIndex = state.works.findIndex(w => w.id === id);
                if (workIndex !== -1 && result.data) {
                    state.works[workIndex] = {
                        ...state.works[workIndex],
                        state: 10,
                        path: result.data.path,
                        response_data: result.data.response_data
                    };
                }
                renderGallery();
            } else if (result.status === 'pending') {
                showToast('warning', '任务还在处理中，已加入轮询队列');
                pollingTasks.add(id);
                startPolling();
                closeTaskDetail();
            } else {
                // 显示详细信息
                const debugInfo = result.debug || {};
                const msg = `请求URL: ${debugInfo.request_url || 'N/A'}\n请求数据: ${JSON.stringify(debugInfo.request_data || {}, null, 2)}\n响应: ${JSON.stringify(debugInfo.response || result, null, 2)}`;
                showToast('error', msg, true);
            }
        } else {
            showToast('error', result.msg || '获取失败', true);
        }
    } catch (error) {
        showToast('error', '获取失败：' + error.message, true);
    } finally {
        btn.textContent = originalText;
        btn.disabled = false;
    }
}

// Toast 通知系统
function showToast(type, message, persistent = false) {
    const container = document.getElementById('toast-container');
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icon = type === 'success' ? '✓' : type === 'warning' ? '⚠' : '✕';
    const title = type === 'success' ? '成功' : type === 'warning' ? '警告' : '错误';
    
    toast.innerHTML = `
        <div class="toast-header">
            <span class="toast-icon">${icon}</span>
            <span class="toast-title">${title}</span>
            <button class="toast-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
        <div class="toast-body">${message}</div>
    `;
    
    container.appendChild(toast);
    
    // 触发动画
    setTimeout(() => toast.classList.add('show'), 10);
    
    // 自动关闭（非持久化）
    if (!persistent) {
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 15000);
    }
}

// 删除任务
async function deleteTask(id) {
    if (!confirm(t('messages.confirmDelete'))) return;
    
    try {
        const response = await fetch(`/api/admin/delete/${id}`, {method: 'POST'});
        const result = await response.json();
        if (result.success) {
            closeTaskDetail();
            await loadWorks();
        } else {
            showErrorModal(t('messages.generateFailed') + '：' + result.error);
        }
    } catch (error) {
        showErrorModal(t('messages.generateFailed') + '：' + error.message);
    }
}

// 渲染上传的图片
function renderUploadedImages() {
    if (state.uploadedImages.length === 0) {
        elements.editorUpload.style.display = 'none';
        elements.uploadBtn.style.display = 'flex';
        return;
    }
    
    elements.editorUpload.style.display = 'flex';
    elements.uploadBtn.style.display = 'none';
    
    let html = state.uploadedImages.map((img, index) => {
        // 获取图片预览 src
        let imgSrc = '';
        if (img.base64) {
            imgSrc = img.base64;
        } else if (img.url) {
            imgSrc = img.url;
        } else if (img.relative_path) {
            // 相对路径可以直接用于预览（前端有路由）
            imgSrc = img.relative_path;
        } else if (img.file_path) {
            // 本地路径无法直接预览，使用占位图
            imgSrc = 'data:image/svg+xml,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><rect fill="#f3f4f6" width="100" height="100"/><text x="50" y="50" text-anchor="middle" dy=".3em" fill="#6b7280" font-size="12">本地</text></svg>');
        }
        
        const title = img.uploaded ? '已上传: ' + (img.url || '') : img.name;
        
        return `
            <div class="upload-item ${img.uploaded ? 'uploaded' : ''}">
                <img src="${imgSrc}" alt="${img.name}" title="${title}" onerror="this.src='data:image/svg+xml,${encodeURIComponent('<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"100\" height=\"100\"><rect fill=\"#fee2e2\" width=\"100\" height=\"100\"/><text x=\"50\" y=\"50\" text-anchor=\"middle\" dy=\".3em\" fill=\"#ef4444\" font-size=\"10\">加载失败</text></svg>')}'">
                ${img.uploaded ? '<div class="upload-badge">✓</div>' : ''}
                <button class="remove" onclick="removeUploadedImage(${index})">×</button>
            </div>
        `;
    }).join('');
    
    if (state.uploadedImages.length < MAX_IMAGES) {
        html += `
            <div class="upload-item upload-add-btn" onclick="document.getElementById('file-input').click()">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
            </div>
        `;
    }
    
    // 添加测试上传按钮
    const hasUnuploaded = state.uploadedImages.some(img => !img.uploaded);
    if (hasUnuploaded) {
        html += `
            <div class="upload-item upload-test-btn" style="display:none" onclick="testUpload()" title="测试上传（不提交生成任务）">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="17 8 12 3 7 8"></polyline>
                    <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
            </div>
        `;
    }
    
    elements.editorUpload.innerHTML = html;
}

// 移除上传的图片
function removeUploadedImage(index) {
    state.uploadedImages.splice(index, 1);
    renderUploadedImages();
}

// 处理图片上传
function handleImageUpload(files) {
    const fileArray = Array.from(files);
    if (fileArray.length === 0) return;
    
    const currentCount = state.uploadedImages.length;
    const availableSlots = MAX_IMAGES - currentCount;
    
    if (availableSlots <= 0) {
        showErrorModal(t('messages.maxImages'));
        return;
    }
    
    let filesToProcess = fileArray;
    
    if (fileArray.length > availableSlots) {
        showErrorModal(t('messages.maxImagesSelect').replace('{n}', availableSlots));
        filesToProcess = fileArray.slice(0, availableSlots);
    }
    
    filesToProcess.forEach(file => {
        const reader = new FileReader();
        reader.onload = (event) => {
            state.uploadedImages.push({
                name: file.name,
                base64: event.target.result,
                file: file,
                uploaded: false,  // 是否已上传到服务器
                url: null         // 上传后的 URL
            });
            renderUploadedImages();
        };
        reader.readAsDataURL(file);
    });
}

// 上传单张图片到服务器
async function uploadImageToServer(imgData) {
    try {
        // 构建上传请求数据，支持多种格式
        const uploadData = { 
            name: imgData.name,
            platform_token: localStorage.getItem('banana_platform_token') || ''
        };
        
        if (imgData.base64) {
            uploadData.base64 = imgData.base64;
        } else if (imgData.file_path) {
            uploadData.file_path = imgData.file_path;
        } else if (imgData.relative_path) {
            uploadData.relative_path = imgData.relative_path;
        } else if (imgData.url) {
            uploadData.url = imgData.url;
        } else {
            throw new Error('图片缺少有效数据');
        }
        
        console.log('📤 uploadImageToServer 上传数据:', uploadData);
        
        const response = await fetch('/api/upload', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(uploadData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            return {
                success: true,
                url: result.url,
                cached: result.cached,
                hash: result.hash
            };
        } else {
            return {
                success: false,
                error: result.error || '上传失败'
            };
        }
    } catch (error) {
        return {
            success: false,
            error: error.message
        };
    }
}

// 查看作品
async function viewWork(id) {
    // 保存任务ID到全局变量，供组件使用
    window._winViewerId = id;
    
    // 加载组件并插入到body
    try {
        const response = await fetch('/components/viewer.html');
        const html = await response.text();
        
        // 移除旧的viewer
        $('#viewer-layer').remove();
        
        // 插入新的viewer
        $('body').append(html);
    } catch (error) {
        console.error('加载viewer组件失败:', error);
    }
}

// 切换viewer显示的图片
function switchViewerImage(src) {
    elements.viewerImage.src = src;
    state.currentViewerImage = src;
}

// 更新编辑器切换按钮状态
function updateEditorToggleState() {
    const btn = document.getElementById('btn-editor');
    if (btn) {
        if (elements.editor.style.display === 'none') {
            btn.classList.remove('active');
        } else {
            btn.classList.add('active');
        }
    }
}

// 生成分辨率图标
function generateRatioIcon(ratio) {
    const parts = ratio.split(':').map(Number);
    if (parts.length !== 2) return '<div class="ratio-icon"><div class="ratio-box"></div></div>';
    
    const [w, h] = parts;
    const maxSize = 14;
    let width, height;
    
    if (w >= h) {
        width = maxSize;
        height = Math.round(maxSize * h / w);
    } else {
        height = maxSize;
        width = Math.round(maxSize * w / h);
    }
    
    return `<div class="ratio-icon" style="width:${maxSize}px;height:${maxSize}px;">
        <div class="ratio-box" style="width:${width}px;height:${height}px;"></div>
    </div>`;
}

// 生成切割图标
function generateCutIcon(num) {
    if (num === 1) return '<div class="cut-icon"><div class="cut-box single"></div></div>';
    
    let cols, rows;
    if (num === 2) { cols = 2; rows = 1; }
    else if (num === 4) { cols = 2; rows = 2; }
    else if (num === 6) { cols = 3; rows = 2; }
    else if (num === 9) { cols = 3; rows = 3; }
    else { cols = 1; rows = 1; }
    
    let boxes = '';
    for (let i = 0; i < num; i++) boxes += '<div class="cut-box"></div>';
    
    return `<div class="cut-icon cols-${cols} rows-${rows}">${boxes}</div>`;
}

// 加载参数
async function loadParameters() {
    try {
        const response = await fetch('/api/get_set');
        const data = await response.json();
        
        if (!data.success) {
            console.error('加载配置失败:', data.error);
            return;
        }
        
        state.config = data.data;
        const config = data.data;
        
        // 模型列表
        const modelMenu = document.getElementById('model-menu');
        modelMenu.innerHTML = config.models.map((m, i) => `
            <div class="param-item" onclick="selectModel(${i})">
                <span class="param-item-icon">${m.logo}</span>
                <span class="param-item-text">${m.name}</span>
            </div>
        `).join('');
        
        // 语言列表
        if (config.languages) {
            const langMenu = document.getElementById('lang-menu');
            langMenu.innerHTML = config.languages.map(lang => `
                <div class="lang-item" data-lang="${lang.code}">${lang.name}</div>
            `).join('');
            
            // 重新绑定语言选项点击事件
            document.querySelectorAll('.lang-item').forEach(item => {
                item.onclick = () => switchLanguage(item.getAttribute('data-lang'));
            });
        }
        
        updateModelDisplay();
        updateSizeOptions();
        updateQualityOptions();
        updateCutOptions();
        
    } catch (error) {
        console.error('加载参数失败:', error);
    }
}

// 更新模型显示
function updateModelDisplay() {
    const config = state.config;
    if (!config || !config.models[state.selectedModel]) return;
    
    const model = config.models[state.selectedModel];
    document.getElementById('model-btn').innerHTML = `
        <span class="param-icon">${model.logo}</span>
        <span class="param-text">${model.name}</span>
    `;
}

// 获取可用的分辨率列表（优先使用 resolutions，否则从模型 size 生成）
function getAvailableResolutions(config, model) {
    if (config.resolutions && config.resolutions.length > 0) {
        return config.resolutions;
    }
    // 从模型 size 数组生成 resolutions
    if (model.size && model.size.length > 0) {
        return model.size.map(ratio => ({ name: ratio, ratio: ratio }));
    }
    return [];
}

// 获取可用的质量列表（优先使用 qualities，否则从模型 quality 生成）
function getAvailableQualities(config, model) {
    if (config.qualities && config.qualities.length > 0) {
        return config.qualities;
    }
    // 从模型 quality 数组生成 qualities
    if (model.quality && model.quality.length > 0) {
        return model.quality.map(size => ({ name: size, size: size }));
    }
    return [];
}

// 更新尺寸选项
function updateSizeOptions() {
    const config = state.config;
    if (!config || !config.models[state.selectedModel]) return;
    
    const model = config.models[state.selectedModel];
    const sizeMenu = document.getElementById('size-menu');
    const sizeSelector = document.getElementById('size-selector');
    
    if (!model.size || model.size.length === 0) {
        sizeSelector.style.display = 'none';
        return;
    }
    
    sizeSelector.style.display = 'block';
    
    // 直接使用模型的尺寸数组
    const sizes = model.size;
    
    // 确保选中的索引在有效范围内
    if (state.selectedSize >= sizes.length) {
        state.selectedSize = sizes.length - 1;
    }
    if (state.selectedSize < 0) {
        state.selectedSize = 0;
    }
    
    sizeMenu.innerHTML = sizes.map((s, index) => `
        <div class="param-item" onclick="selectSize(${index})">
            ${generateRatioIcon(s)}
            <span class="param-item-text">${t('sizes.' + s) || s}</span>
        </div>
    `).join('');
    
    updateSizeDisplay();
}

// 更新尺寸显示
function updateSizeDisplay() {
    const config = state.config;
    if (!config || !config.models[state.selectedModel]) return;
    
    const model = config.models[state.selectedModel];
    const sizes = model.size || [];
    if (!sizes[state.selectedSize]) return;
    
    const s = sizes[state.selectedSize];
    document.getElementById('size-btn').innerHTML = `
        ${generateRatioIcon(s)}
        <span class="param-text">${t('sizes.' + s) || s}</span>
    `;
}

// 更新质量选项
function updateQualityOptions() {
    const config = state.config;
    if (!config || !config.models[state.selectedModel]) return;
    
    const model = config.models[state.selectedModel];
    const qualityMenu = document.getElementById('quality-menu');
    const qualitySelector = document.getElementById('quality-selector');
    
    if (!model.quality || model.quality.length === 0) {
        qualitySelector.style.display = 'none';
        return;
    }
    
    qualitySelector.style.display = 'block';
    
    // 直接使用模型的质量数组
    const qualities = model.quality;
    
    // 确保选中的索引在有效范围内
    if (state.selectedQuality >= qualities.length) {
        state.selectedQuality = qualities.length - 1;
    }
    if (state.selectedQuality < 0) {
        state.selectedQuality = 0;
    }
    
    qualityMenu.innerHTML = qualities.map((q, index) => `
        <div class="param-item" onclick="selectQuality(${index})">
            <icon class="quality-icon icon icon-fenbianshuai"></icon>
            <span class="param-item-text">${t('qualities.' + q) || q}</span>
        </div>
    `).join('');
    
    updateQualityDisplay();
}

// 更新质量显示
function updateQualityDisplay() {
    const config = state.config;
    if (!config || !config.models[state.selectedModel]) return;
    
    const model = config.models[state.selectedModel];
    const qualities = model.quality || [];
    if (!qualities[state.selectedQuality]) return;
    
    const q = qualities[state.selectedQuality];
    document.getElementById('quality-btn').innerHTML = `
        <icon class="quality-icon icon icon-fenbianshuai"></icon>
        <span class="param-text">${t('qualities.' + q) || q}</span>
    `;
}

// 更新切割选项
function updateCutOptions() {
    const config = state.config;
    if (!config || !config.models[state.selectedModel]) return;
    
    const model = config.models[state.selectedModel];
    const cutMenu = document.getElementById('cut-menu');
    const cutSelector = document.getElementById('cut-selector');
  
    if (!model.cut || model.cut.length === 0) {
        cutSelector.style.display = 'none';
        state.selectedCut = 1;
        return;
    }
    
    cutSelector.style.display = 'block';
    
    if (!model.cut.includes(state.selectedCut)) {
        state.selectedCut = model.cut[0] || 1;
    }
    
    const cutLabels = {
        1: t('params.noCut'),
        2: '2' + t('params.grid'),
        4: '4' + t('params.grid'),
        6: '6' + t('params.grid'),
        9: '9' + t('params.grid')
    };
    
    cutMenu.innerHTML = model.cut.map(value => `
        <div class="param-item" onclick="selectCut(${value})">
            ${generateCutIcon(value)}
            <span class="param-item-text">${cutLabels[value] || value + t('params.grid')}</span>
        </div>
    `).join('');
    
    updateCutDisplay();
}

// 更新切割显示
function updateCutDisplay() {
    const cutLabels = {
        1: t('params.noCut'),
        2: '2' + t('params.grid'),
        4: '4' + t('params.grid'),
        6: '6' + t('params.grid'),
        9: '9' + t('params.grid')
    };
    
    document.getElementById('cut-btn').innerHTML = `
        ${generateCutIcon(state.selectedCut)}
        <span class="param-text">${cutLabels[state.selectedCut] || state.selectedCut + t('params.grid')}</span>
    `;
}

// 选择模型
function selectModel(index) {
    state.selectedModel = index;
    localStorage.setItem('banana_selected_model', index.toString());
    
    updateModelDisplay();
    updateSizeOptions();
    updateQualityOptions();
    updateCutOptions();
    
    closeAllMenus();
}

// 选择尺寸
function selectSize(index) {
    state.selectedSize = index;
    localStorage.setItem('banana_selected_size', index.toString());
    updateSizeDisplay();
    closeAllMenus();
}

// 选择质量
function selectQuality(index) {
    state.selectedQuality = index;
    localStorage.setItem('banana_selected_quality', index.toString());
    updateQualityDisplay();
    closeAllMenus();
}

// 选择切割
function selectCut(value) {
    state.selectedCut = value;
    localStorage.setItem('banana_selected_cut', value.toString());
    updateCutDisplay();
    closeAllMenus();
}

// 关闭所有菜单
function closeAllMenus() {
    document.querySelectorAll('.param-menu').forEach(menu => menu.classList.remove('show'));
    elements.langMenu.classList.remove('show');
}

// 提交生成
async function submit() {
    const prompt = elements.editorInput.textContent.trim();
    if (!prompt) {
        showErrorModal(t('messages.promptRequired'));
        return;
    }
    
    // 从localStorage获取配置
    const apiKey = localStorage.getItem('banana_api_key') || '';
    const platformToken = localStorage.getItem('banana_platform_token') || '';
    const modelApiKey = localStorage.getItem('banana_model_api_key') || '';
    
    if (!apiKey) {
        showSettings();
        return;
    }
    
    elements.submitBtn.disabled = true;
    elements.submitBtn.innerHTML = '<div class="spinner" style="width:20px;height:20px;border-width:2px;"></div>';
    
    try {
        const config = state.config;
        const currentModel = config?.models?.[state.selectedModel];
        const model = currentModel?.model || 'nano-banana-pro';
        
        // 尺寸和质量直接从模型配置中获取用户选择的值
        const modelSizes = currentModel?.size || ['1:1'];
        const modelQualities = currentModel?.quality || ['1K', '2K', '4K'];
        
        const ratio = modelSizes[state.selectedSize] || '1:1';
        const quality = modelQualities[state.selectedQuality] || '2K';
        
        // 调试日志
        console.log('📊 提交参数:', {
            selectedSize: state.selectedSize,
            selectedQuality: state.selectedQuality,
            modelSizes: modelSizes,
            modelQualities: modelQualities,
            ratio: ratio,
            quality: quality
        });
        const platformToken = localStorage.getItem('banana_platform_token') || '';
        // 先上传图片获取URL
        let imageUrls = [];
        if (state.uploadedImages.length > 0) {
            if (!platformToken) {
                showErrorModal('图生图功能需要配置 Platform Token');
                elements.submitBtn.disabled = false;
                elements.submitBtn.innerHTML = `
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="22" y1="2" x2="11" y2="13"></line>
                        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                    </svg>
                `;
                return;
            }
            
            console.log(`📤 上传 ${state.uploadedImages.length} 张图片...`);
            
            
          
            for (const img of state.uploadedImages) {
                try {
                    // 构建上传请求数据，支持多种格式
                    const uploadData = { 
                        name: img.name,
                        platform_token: platformToken
                    };
                    
                    if (img.base64) {
                        uploadData.base64 = img.base64;
                    } else if (img.file_path) {
                        uploadData.file_path = img.file_path;
                    } else if (img.relative_path) {
                        uploadData.relative_path = img.relative_path;
                    } else if (img.url) {
                        uploadData.url = img.url;
                    } else {
                        console.error('图片缺少有效数据:', img.name);
                        continue;
                    }
                    
                    const uploadResponse = await fetch('/api/upload', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(uploadData)
                    });
                    
                    const uploadResult = await uploadResponse.json();
                    
                    if (uploadResult.success && uploadResult.url) {
                        imageUrls.push(uploadResult.url);
                        console.log(`✅ 图片上传成功: ${uploadResult.url} (缓存: ${uploadResult.cached})`);
                    } else {
                        console.error('图片上传失败:', uploadResult.error);
                        showErrorModal(`图片上传失败: ${uploadResult.error}`);
                        elements.submitBtn.disabled = false;
                        elements.submitBtn.innerHTML = `
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="22" y1="2" x2="11" y2="13"></line>
                                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                            </svg>
                        `;
                        return;
                    }
                } catch (uploadErr) {
                    console.error('图片上传异常:', uploadErr);
                    showErrorModal(`图片上传异常: ${uploadErr.message}`);
                    elements.submitBtn.disabled = false;
                    elements.submitBtn.innerHTML = `
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    `;
                    return;
                }
            }
            
            console.log(`✅ 所有图片上传完成，URLs:`, imageUrls);
        }
        
        const requestData = {
            // 配置信息
            api_key: apiKey,
            platform_token: platformToken,
            model_api_key: modelApiKey,
            save_path: localStorage.getItem('banana_save_path') || '',
            // 生成参数
            prompt,
            model: model,
            ratio: ratio,
            quality: quality,
            cut: state.selectedCut,
            // 已上传的图片URLs
            image_urls: imageUrls
        };
        console.log(requestData)
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(requestData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // 清除保存的提示词
            clearPendingPrompt();
            elements.editorInput.textContent = '';
            state.uploadedImages = [];
            renderUploadedImages();
            await loadWorks();
            
            // 将新任务加入轮询队列
            if (result.work_id) {
                pollingTasks.add(result.work_id);
                startPolling();
                console.log(`📋 任务 ${result.work_id} 已加入轮询队列`);
            }
        } else {
            showErrorModal(result.error || result.message || JSON.stringify(result, null, 2));
        }
    } catch (error) {
        showErrorModal(t('messages.generateFailed') + '：' + error.message);
    } finally {
        elements.submitBtn.disabled = false;
        elements.submitBtn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
        `;
    }
}

// 设置事件监听
function setupEventListeners() {
    // Logo点击
    document.getElementById('logo-btn').onclick = showAboutModal;
    
    // 关闭服务
    document.getElementById('btn-close').onclick = async () => {
        if (confirm(t('messages.confirmClose'))) {
            await fetch('/api/shutdown', {method: 'POST'});
            window.close();
        }
    };
    
    // 设置按钮
    document.getElementById('btn-settings').onclick = showSettings;
    
    // 主题切换
    document.getElementById('btn-theme').onclick = () => {
        state.darkMode = !state.darkMode;
        document.body.classList.toggle('dark', state.darkMode);
        updateThemeIcon();
        saveThemeState();
    };
    
    // 语言选择
    document.getElementById('btn-lang').onclick = (e) => {
        e.stopPropagation();
        closeAllMenus();
        elements.langMenu.classList.toggle('show');
    };
    
    // 语言选项点击
    document.querySelectorAll('.lang-item').forEach(item => {
        item.onclick = () => switchLanguage(item.getAttribute('data-lang'));
    });
    
    // 搜索框
    elements.searchInput.oninput = (e) => searchWorks(e.target.value);
    
    // 编辑器切换
    document.getElementById('btn-editor').onclick = () => {
        state.showEditor = !state.showEditor;
        elements.editor.style.display = state.showEditor ? 'block' : 'none';
        document.getElementById('btn-editor').classList.toggle('active', state.showEditor);
    };
    
    // AI提示词按钮
    document.getElementById('ai-prompt-btn').onclick = showPromptModal;
    
    // 文件上传
    elements.uploadBtn.onclick = () => elements.fileInput.click();
    
    // 编辑器输入监听 - 用户键盘输入时保存到 localStorage
    elements.editorInput.addEventListener('keyup', function() {
        const prompt = this.textContent.trim();
        if (prompt) {
            localStorage.setItem('banana_pending_prompt', prompt);
        } else {
            localStorage.removeItem('banana_pending_prompt');
        }
    });
    elements.fileInput.onchange = (e) => {
        handleImageUpload(e.target.files);
        e.target.value = '';
    };
    
    // 提交
    elements.submitBtn.onclick = submit;
    
    // 参数菜单
    document.getElementById('model-btn').onclick = (e) => {
        e.stopPropagation();
        closeAllMenus();
        document.getElementById('model-menu').classList.toggle('show');
    };
    
    document.getElementById('size-btn').onclick = (e) => {
        e.stopPropagation();
        closeAllMenus();
        document.getElementById('size-menu').classList.toggle('show');
    };
    
    document.getElementById('quality-btn').onclick = (e) => {
        e.stopPropagation();
        closeAllMenus();
        document.getElementById('quality-menu').classList.toggle('show');
    };
    
    document.getElementById('cut-btn').onclick = (e) => {
        e.stopPropagation();
        closeAllMenus();
        document.getElementById('cut-menu').classList.toggle('show');
    };
    
    // 查看器
    document.getElementById('viewer-close').onclick = () => {
        elements.viewer.style.display = 'none';
        elements.editor.style.display = 'block';
        updateEditorToggleState();
    };
    
    // 信息按钮
    document.getElementById('action-info').onclick = () => {
        if (!state.selectedWork) return;
        showTaskDetail(state.selectedWork.id);
        elements.viewer.style.display = 'none';
    };
    
    // 打开文件夹
    document.getElementById('action-folder').onclick = async () => {
        if (!state.selectedWork) return;
        try {
            const response = await fetch('/api/open-folder', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ path: state.selectedWork.path })
            });
            const result = await response.json();
            if (!result.success) showToast('error', result.error);
        } catch (error) {
            showToast('error', error.message);
        }
    };
    
    // 编辑按钮
    document.getElementById('action-edit').onclick = () => {
        if (!state.selectedWork) return;
        elements.editorInput.textContent = state.selectedWork.prompt;
        elements.viewer.style.display = 'none';
        elements.editor.style.display = 'block';
        updateEditorToggleState();
    };
    
    // 点击外部关闭菜单
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.param-selector') && !e.target.closest('.lang-selector')) {
            closeAllMenus();
        }
    });
    
    // 点击弹窗背景关闭
    document.querySelectorAll('.modal').forEach(modal => {
        modal.onclick = (e) => {
            if (e.target === modal) modal.style.display = 'none';
        };
    });
    
    // 键盘快捷键
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (elements.viewer.style.display === 'flex') {
                elements.viewer.style.display = 'none';
                elements.editor.style.display = 'block';
            } else {
                hideAllModals();
            }
        }
        
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            if (elements.editorInput.textContent.trim()) submit();
        }
    });
}

// 启动应用
init();
