/**
 * AI前沿哨兵 - WebUI主脚本
 * 信息源管理、采集控制、报告生成
 * 
 * 功能：
 * - 多视图导航切换
 * - 信息源管理（内置+自定义）
 * - 预设快速添加模板
 * - 分类筛选
 * - 采集与报告生成
 */

// ============================================
// 应用状态管理
// ============================================
const state = {
    currentView: 'dashboard',      // 当前视图
    sources: [],                     // 用户自定义信息源
    logs: [],                        // 采集日志
    stats: {                         // 统计数据
        github: 0,
        arxiv: 0,
        hn: 0,
        blogs: 0
    },
    keywords: [],                    // 关注关键词
    settings: {                      // 系统设置
        twitterToken: '',
        morningEnabled: true,
        eveningEnabled: true
    }
};

// ============================================
// 内置信息源配置（不可删除）
// ============================================
const builtInSources = [
    {
        id: 'github',
        name: 'GitHub Trending',
        description: '追踪全球AI开源项目的热门榜单，发现最新最热门的开源项目',
        icon: '⌘',
        category: 'tech-community',
        detail: '采集GitHub上AI相关项目的Star、Fork数据，适合发现新兴项目'
    },
    {
        id: 'arxiv',
        name: 'arXiv 论文',
        description: '获取人工智能、机器学习领域的最新学术研究论文',
        icon: '◉',
        category: 'academic',
        detail: '覆盖cs.AI、cs.LG、cs.CL等分类的学术论文'
    },
    {
        id: 'hackernews',
        name: 'Hacker News',
        description: '了解全球开发者社区讨论的AI热点话题和行业动态',
        icon: '◈',
        category: 'tech-community',
        detail: '来自Y Combinator的开发者社区，涵盖技术、创业、AI讨论'
    },
    {
        id: 'twitter',
        name: 'Twitter/X',
        description: '追踪AI大咖和机构的最新动态和见解',
        icon: '✕',
        category: 'social',
        detail: '需要配置Twitter Bearer Token才能使用'
    },
    {
        id: 'blogs',
        name: 'RSS 订阅源',
        description: '订阅任意博客的新闻更新，通过RSS协议获取内容',
        icon: '◎',
        category: 'blog',
        detail: '支持任何提供RSS/Atom订阅的网站'
    }
];

// ============================================
// 快速添加预设模板
// ============================================
const quickAddTemplates = [
    {
        name: 'OpenAI 官方博客',
        url: 'https://openai.com/blog/rss.xml',
        description: '获取OpenAI最新产品发布和技术研究',
        icon: '🤖',
        category: 'official-blog',
        tags: ['官方', 'AI公司', 'GPT']
    },
    {
        name: 'Anthropic 官方博客',
        url: 'https://www.anthropic.com/news/rss',
        description: '了解Claude和Anthropic的最新动态',
        icon: '🧠',
        category: 'official-blog',
        tags: ['官方', 'AI公司', 'Claude']
    },
    {
        name: 'Google AI Blog',
        url: 'https://blog.google/technology/ai/rss/',
        description: 'Google在AI领域的研究进展和产品应用',
        icon: '🔍',
        category: 'official-blog',
        tags: ['官方', 'AI公司', 'Google']
    },
    {
        name: 'DeepMind 研究',
        url: 'https://deepmind.com/blog/feed/basic/',
        description: 'DeepMind的前沿AI研究成果',
        icon: '💡',
        category: 'official-blog',
        tags: ['官方', 'AI公司', '研究']
    },
    {
        name: 'Meta AI 研究',
        url: 'https://ai.meta.com/blog/rss/',
        description: 'Meta在AI领域的开源研究和技术分享',
        icon: '🔷',
        category: 'official-blog',
        tags: ['官方', 'AI公司', '开源']
    },
    {
        name: 'Machine Learning Mastery',
        url: 'https://machinelearningmastery.com/feed/',
        description: '实用的机器学习教程和最佳实践',
        icon: '📊',
        category: 'tutorial',
        tags: ['教程', '机器学习', '实践']
    },
    {
        name: 'Towards Data Science',
        url: 'https://towardsdatascience.com/feed',
        description: '数据科学和机器学习的中文精选文章',
        icon: '📝',
        category: 'tutorial',
        tags: ['博客', '数据科学', '精选']
    },
    {
        name: 'Hugging Face Blog',
        url: 'https://huggingface.co/blog/feed.xml',
        description: '开源LLM和模型库的最新动态',
        icon: '🤗',
        category: 'official-blog',
        tags: ['官方', '开源', 'LLM']
    }
];

// ============================================
// 信息源分类配置
// ============================================
const sourceCategories = [
    { id: 'all', name: '全部', icon: '📦', description: '显示所有信息源' },
    { id: 'official-blog', name: '官方博客', icon: '🏢', description: 'AI公司官方发布的博客' },
    { id: 'tech-community', name: '技术社区', icon: '💬', description: '开发者社区和技术论坛' },
    { id: 'academic', name: '学术论文', icon: '📚', description: '学术机构发表的论文' },
    { id: 'social', name: '社交媒体', icon: '🌐', description: '社交平台上的AI讨论' },
    { id: 'tutorial', name: '教程博客', icon: '📖', description: '学习教程和技术博客' },
    { id: 'custom', name: '自定义', icon: '✏️', description: '您自己添加的信息源' }
];

// 模拟数据（实际使用时替换为真实API调用）
const mockData = {
    github: [
        { title: 'microsoft/DeepSeek-V3', stars: 24500, forks: 2800, description: 'DeepSeek V3: A Powerful MoE LLM', language: 'Python' },
        { title: 'anthropics/anthropic-cookbook', stars: 8200, forks: 890, description: 'A collection of notebooks', language: 'Jupyter' },
        { title: 'openai/openai-o3', stars: 15600, forks: 1200, description: 'Next generation AI model', language: 'Python' }
    ],
    arxiv: [
        { title: 'Attention Is All You Need', authors: 'Vaswani et al.', abstract: 'We propose a new architecture...' },
        { title: 'GPT-4 Technical Report', authors: 'OpenAI Team', abstract: 'We report the development of GPT-4...' }
    ],
    hackernews: [
        { title: 'Show HN: I built an AI coding assistant', score: 892, comments: 234 },
        { title: 'Ask HN: Best practices for LLM deployment?', score: 567, comments: 189 }
    ],
    blogs: [
        { title: 'Anthropic News: Claude 3.5 Release', author: 'Anthropic Team', published: '2小时前' },
        { title: 'OpenAI Blog: New API Features', author: 'OpenAI', published: '5小时前' }
    ]
};

// ============================================
// 初始化
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    // 从本地存储加载数据
    loadFromStorage();
    
    // 初始化各模块
    initNavigation();
    initSources();
    initSettings();
    initActions();
    initAddSourceForm();
    
    // 更新UI
    updateTime();
    loadMockData();
    
    // 定时更新
    setInterval(updateTime, 1000);
});

// ============================================
// 本地存储管理
// ============================================
function loadFromStorage() {
    // 加载自定义信息源
    const savedSources = localStorage.getItem('sentinel-custom-sources');
    if (savedSources) {
        state.sources = JSON.parse(savedSources);
    }
    
    // 加载关键词
    const savedKeywords = localStorage.getItem('sentinel-keywords');
    if (savedKeywords) {
        state.keywords = JSON.parse(savedKeywords);
    }
    
    // 加载设置
    const savedSettings = localStorage.getItem('sentinel-settings');
    if (savedSettings) {
        state.settings = { ...state.settings, ...JSON.parse(savedSettings) };
    }
}

function saveToStorage() {
    localStorage.setItem('sentinel-custom-sources', JSON.stringify(state.sources));
    localStorage.setItem('sentinel-keywords', JSON.stringify(state.keywords));
    localStorage.setItem('sentinel-settings', JSON.stringify(state.settings));
}

// ============================================
// 导航切换
// ============================================
function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const views = document.querySelectorAll('.view');
    const viewTitle = document.getElementById('viewTitle');
    
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const viewName = item.dataset.view;
            
            // 更新导航状态
            navItems.forEach(n => n.classList.remove('active'));
            item.classList.add('active');
            
            // 更新视图
            views.forEach(v => v.classList.remove('active'));
            document.getElementById(`${viewName}View`).classList.add('active');
            
            // 更新标题
            const titles = {
                dashboard: '概览',
                sources: '信息源',
                reports: '报告',
                settings: '配置'
            };
            viewTitle.textContent = titles[viewName] || viewName;
            
            state.currentView = viewName;
            
            // 如果是信息源视图，刷新显示
            if (viewName === 'sources') {
                renderSources();
            }
        });
    });
}

// ============================================
// 信息源管理
// ============================================
function initSources() {
    renderSources();
}

function renderSources(filter = 'all') {
    const grid = document.getElementById('sourcesGrid');
    grid.innerHTML = '';
    
    // 根据分类筛选
    let filteredBuiltIn = builtInSources;
    if (filter !== 'all') {
        if (filter === 'custom') {
            // 显示自定义源
            renderCustomSources(grid);
            return;
        }
        filteredBuiltIn = builtInSources.filter(s => s.category === filter);
    }
    
    // 渲染内置信息源
    filteredBuiltIn.forEach(config => {
        const source = state.sources.find(s => s.id === config.id) || { enabled: true, count: 0 };
        const card = createSourceCard(config, source);
        grid.appendChild(card);
    });
    
    // 如果显示全部，再添加自定义源
    if (filter === 'all') {
        renderCustomSources(grid);
    }
}

function renderCustomSources(container) {
    // 添加自定义源标题
    if (state.sources.length > 0) {
        const customTitle = document.createElement('div');
        customTitle.className = 'sources-section-title';
        customTitle.innerHTML = `<span class="sources-section-icon">✏️</span> 自定义信息源 <span class="sources-count">${state.sources.length}</span>`;
        container.appendChild(customTitle);
    }
    
    state.sources.forEach(source => {
        const card = createCustomSourceCard(source);
        container.appendChild(card);
    });
    
    // 如果没有自定义源，显示提示
    if (state.sources.length === 0) {
        const emptyHint = document.createElement('div');
        emptyHint.className = 'sources-empty-hint';
        emptyHint.innerHTML = `
            <p>还没有添加自定义信息源</p>
            <p class="hint-sub">点击上方的"添加信息源"按钮，或使用下方的快速添加模板</p>
        `;
        container.appendChild(emptyHint);
    }
}

function createSourceCard(config, source) {
    const card = document.createElement('div');
    card.className = 'source-card';
    card.id = `source-${config.id}`;
    
    // 获取分类标签
    const category = sourceCategories.find(c => c.id === config.category) || sourceCategories[0];
    
    card.innerHTML = `
        <div class="source-card-header">
            <div class="source-title-row">
                <span class="source-icon">${config.icon}</span>
                <span class="source-name">${config.name}</span>
            </div>
            <label class="source-toggle">
                <input type="checkbox" ${source.enabled ? 'checked' : ''} data-source="${config.id}">
                <span class="toggle-slider"></span>
            </label>
        </div>
        <span class="source-category-tag" data-category="${config.category}">${category.icon} ${category.name}</span>
        <p class="source-description">${config.description}</p>
        <div class="source-detail-hint" title="${config.detail}">
            💡 ${config.detail}
        </div>
        <div class="source-stats">
            <div class="source-stat">
                <div class="source-stat-value" id="count-${config.id}">${source.count}</div>
                <div class="source-stat-label">已采集</div>
            </div>
            <div class="source-stat">
                <div class="source-stat-value">-</div>
                <div class="source-stat-label">上次采集</div>
            </div>
        </div>
        <div class="source-card-actions">
            <button class="source-btn" onclick="collectSource('${config.id}')">立即采集</button>
        </div>
    `;
    
    // 开关事件
    const toggle = card.querySelector('input[type="checkbox"]');
    toggle.addEventListener('change', (e) => {
        source.enabled = e.target.checked;
        showToast(`${config.name}已${source.enabled ? '启用' : '禁用'}`, 'success');
    });
    
    return card;
}

function createCustomSourceCard(source) {
    const card = document.createElement('div');
    card.className = 'source-card source-card-custom';
    card.id = `custom-source-${source.id}`;
    
    card.innerHTML = `
        <div class="source-card-header">
            <div class="source-title-row">
                <span class="source-icon">🔗</span>
                <span class="source-name">${source.name}</span>
            </div>
            <label class="source-toggle">
                <input type="checkbox" ${source.enabled ? 'checked' : ''} data-source="custom-${source.id}">
                <span class="toggle-slider"></span>
            </label>
        </div>
        <span class="source-category-tag" data-category="custom">✏️ 自定义</span>
        <p class="source-description">${source.description || '自定义RSS订阅源'}</p>
        <div class="source-url-preview">
            <span class="url-label">订阅地址:</span>
            <span class="url-value" title="${source.url}">${truncateUrl(source.url)}</span>
        </div>
        ${source.tags && source.tags.length > 0 ? `
        <div class="source-tags">
            ${source.tags.map(tag => `<span class="source-tag">${tag}</span>`).join('')}
        </div>
        ` : ''}
        <div class="source-stats">
            <div class="source-stat">
                <div class="source-stat-value" id="count-custom-${source.id}">${source.count || 0}</div>
                <div class="source-stat-label">已采集</div>
            </div>
            <div class="source-stat">
                <div class="source-stat-value">-</div>
                <div class="source-stat-label">上次采集</div>
            </div>
        </div>
        <div class="source-card-actions">
            <button class="source-btn" onclick="collectCustomSource('${source.id}')">采集</button>
            <button class="source-btn source-btn-danger" onclick="deleteCustomSource('${source.id}')">删除</button>
        </div>
    `;
    
    // 开关事件
    const toggle = card.querySelector('input[type="checkbox"]');
    toggle.addEventListener('change', (e) => {
        source.enabled = e.target.checked;
        showToast(`${source.name}已${source.enabled ? '启用' : '禁用'}`, 'success');
        saveToStorage();
    });
    
    return card;
}

function truncateUrl(url, maxLength = 40) {
    if (url.length <= maxLength) return url;
    return url.substring(0, maxLength) + '...';
}

// 采集自定义源
async function collectCustomSource(sourceId) {
    showLoading(true);
    const source = state.sources.find(s => s.id === sourceId);
    if (!source) return;
    
    addLog(`开始采集 ${source.name}...`, 'pending');
    await delay(1000);
    
    source.count = (source.count || 0) + 1;
    const countEl = document.getElementById(`count-custom-${sourceId}`);
    if (countEl) countEl.textContent = source.count;
    
    addLog(`${source.name} 采集完成`, 'success');
    showLoading(false);
    showToast(`${source.name} 采集完成`, 'success');
    saveToStorage();
}

// 删除自定义源
function deleteCustomSource(sourceId) {
    const source = state.sources.find(s => s.id === sourceId);
    if (!source) return;
    
    if (confirm(`确定要删除 "${source.name}" 吗？`)) {
        state.sources = state.sources.filter(s => s.id !== sourceId);
        saveToStorage();
        renderSources();
        showToast(`已删除 ${source.name}`, 'success');
    }
}

// ============================================
// 添加信息源表单
// ============================================
function initAddSourceForm() {
    const addBtn = document.getElementById('addSourceBtn');
    const modal = document.getElementById('addSourceModal');
    const closeBtn = document.getElementById('closeModal');
    const form = document.getElementById('addSourceForm');
    const quickAddSection = document.getElementById('quickAddSection');
    
    // 点击添加按钮
    addBtn.addEventListener('click', () => {
        modal.classList.add('active');
        renderQuickAddTemplates();
    });
    
    // 点击关闭
    closeBtn.addEventListener('click', () => {
        modal.classList.remove('active');
    });
    
    // 点击模态框外部关闭
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });
    
    // 表单提交
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        submitCustomSource();
    });
    
    // 分类标签切换
    const categoryTabs = document.querySelectorAll('.category-tab');
    categoryTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            categoryTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            filterQuickAddTemplates(tab.dataset.category);
        });
    });
}

function renderQuickAddTemplates(category = 'all') {
    const container = document.getElementById('quickAddTemplates');
    if (!container) return;
    
    container.innerHTML = '';
    
    const templates = category === 'all' 
        ? quickAddTemplates 
        : quickAddTemplates.filter(t => t.category === category);
    
    templates.forEach(template => {
        // 检查是否已添加
        const isAdded = state.sources.some(s => s.url === template.url);
        
        const card = document.createElement('div');
        card.className = `quick-add-card ${isAdded ? 'added' : ''}`;
        card.innerHTML = `
            <div class="quick-add-icon">${template.icon}</div>
            <div class="quick-add-info">
                <div class="quick-add-name">${template.name}</div>
                <div class="quick-add-desc">${template.description}</div>
                <div class="quick-add-tags">
                    ${template.tags.map(tag => `<span class="quick-tag">${tag}</span>`).join('')}
                </div>
            </div>
            <button class="quick-add-btn ${isAdded ? 'added' : ''}" 
                    ${isAdded ? 'disabled' : ''} 
                    onclick="quickAddSource('${template.url}', '${template.name}', '${template.description}', '${template.icon}')">
                ${isAdded ? '✓ 已添加' : '+ 添加'}
            </button>
        `;
        container.appendChild(card);
    });
}

function filterQuickAddTemplates(category) {
    renderQuickAddTemplates(category);
}

function quickAddSource(url, name, description, icon) {
    // 检查是否已存在
    if (state.sources.some(s => s.url === url)) {
        showToast('该信息源已添加', 'warning');
        return;
    }
    
    const newSource = {
        id: 'custom-' + Date.now(),
        name: name,
        url: url,
        description: description,
        icon: icon,
        enabled: true,
        count: 0,
        tags: []
    };
    
    state.sources.push(newSource);
    saveToStorage();
    renderSources();
    renderQuickAddTemplates();
    
    showToast(`已添加 "${name}"`, 'success');
}

function submitCustomSource() {
    const name = document.getElementById('sourceName').value.trim();
    const url = document.getElementById('sourceUrl').value.trim();
    const description = document.getElementById('sourceDesc').value.trim();
    
    if (!name || !url) {
        showToast('请填写名称和订阅地址', 'error');
        return;
    }
    
    // 简单URL验证
    if (!isValidUrl(url)) {
        showToast('请输入有效的URL地址', 'error');
        return;
    }
    
    // 检查是否已存在
    if (state.sources.some(s => s.url === url)) {
        showToast('该信息源已添加', 'warning');
        return;
    }
    
    const newSource = {
        id: 'custom-' + Date.now(),
        name: name,
        url: url,
        description: description || '自定义RSS订阅源',
        enabled: true,
        count: 0,
        tags: []
    };
    
    state.sources.push(newSource);
    saveToStorage();
    
    // 重置表单
    document.getElementById('addSourceForm').reset();
    document.getElementById('addSourceModal').classList.remove('active');
    
    renderSources();
    showToast(`已添加 "${name}"`, 'success');
}

function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

// ============================================
// 设置管理
// ============================================
function initSettings() {
    const tokenInput = document.getElementById('twitterToken');
    const keywordsInput = document.getElementById('newKeyword');
    const keywordsTags = document.getElementById('keywordsTags');
    
    // 恢复设置值
    tokenInput.value = state.settings.twitterToken || '';
    
    // Token输入
    tokenInput.addEventListener('change', (e) => {
        state.settings.twitterToken = e.target.value;
    });
    
    // 关键词添加
    keywordsInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && e.target.value.trim()) {
            e.preventDefault();
            addKeyword(e.target.value.trim());
            e.target.value = '';
        }
    });
    
    // 调度开关
    document.getElementById('morningEnabled').addEventListener('change', (e) => {
        state.settings.morningEnabled = e.target.checked;
    });
    
    document.getElementById('eveningEnabled').addEventListener('change', (e) => {
        state.settings.eveningEnabled = e.target.checked;
    });
    
    // 保存按钮
    document.getElementById('saveSettingsBtn').addEventListener('click', saveSettings);
    
    // 恢复调度设置
    document.getElementById('morningEnabled').checked = state.settings.morningEnabled;
    document.getElementById('eveningEnabled').checked = state.settings.eveningEnabled;
    
    // 初始化关键词标签
    state.keywords.forEach(kw => addKeyword(kw, false));
}

function addKeyword(keyword, shouldRender = true) {
    if (state.keywords.includes(keyword)) return;
    
    state.keywords.push(keyword);
    
    if (shouldRender) {
        const container = document.getElementById('keywordsTags');
        const tag = document.createElement('span');
        tag.className = 'tag';
        tag.innerHTML = `
            ${keyword}
            <span class="tag-remove" onclick="removeKeyword('${keyword}')">×</span>
        `;
        container.insertBefore(tag, container.lastElementChild);
    }
}

function removeKeyword(keyword) {
    state.keywords = state.keywords.filter(k => k !== keyword);
    const tags = document.querySelectorAll('.tag');
    tags.forEach(tag => {
        if (tag.textContent.trim().startsWith(keyword)) {
            tag.remove();
        }
    });
}

function saveSettings() {
    saveToStorage();
    showToast('配置已保存', 'success');
}

// ============================================
// 操作按钮
// ============================================
function initActions() {
    // 采集按钮
    document.getElementById('collectBtn').addEventListener('click', collectAll);
    
    // 报告按钮
    document.getElementById('reportBtn').addEventListener('click', () => {
        document.querySelector('[data-view="reports"]').click();
    });
    
    document.getElementById('generateReportBtn').addEventListener('click', generateReport);
}

async function collectAll() {
    showLoading(true);
    addLog('开始采集所有信息源...', 'pending');
    
    const statusIndicator = document.querySelector('.status-indicator');
    statusIndicator.classList.add('working');
    document.querySelector('.status-text').textContent = '采集中';
    
    // 模拟采集过程
    await delay(2000);
    
    // 更新统计数据
    state.stats.github = mockData.github.length;
    state.stats.arxiv = mockData.arxiv.length;
    state.stats.hn = mockData.hackernews.length;
    state.stats.blogs = mockData.blogs.length;
    
    // 更新UI
    updateStats();
    
    // 更新信息源卡片
    [...builtInSources, ...state.sources].forEach(config => {
        const count = state.stats[config.id] || config.count || 0;
        const countEl = document.getElementById(`count-${config.id}`);
        if (countEl) countEl.textContent = count;
    });
    
    // 更新热门内容
    updateHotContent();
    
    addLog('采集完成', 'success');
    
    showLoading(false);
    statusIndicator.classList.remove('working');
    document.querySelector('.status-text').textContent = '就绪';
    
    showToast('采集完成', 'success');
}

async function collectSource(sourceId) {
    showLoading(true);
    addLog(`开始采集 ${sourceId}...`, 'pending');
    
    await delay(1000);
    
    // 更新计数
    const mockCounts = { github: 3, arxiv: 2, hackernews: 2, blogs: 2, twitter: 0 };
    state.stats[sourceId] = mockCounts[sourceId] || 0;
    
    const countEl = document.getElementById(`count-${sourceId}`);
    if (countEl) countEl.textContent = state.stats[sourceId];
    
    addLog(`${sourceId} 采集完成`, 'success');
    showLoading(false);
    showToast(`${sourceId} 采集完成`, 'success');
}

function generateReport() {
    const type = document.getElementById('reportType').value;
    const preview = document.getElementById('reportPreview');
    
    // 生成模拟报告内容
    const reportHtml = `
        <div class="report-content">
            <h1>${type === 'morning' ? '🌅' : '🌙'} AI前沿哨兵 - ${new Date().toLocaleDateString('zh-CN')} ${type === 'morning' ? '晨报' : '晚报'}</h1>
            
            <h2>📊 概览</h2>
            <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
                <tr style="border-bottom: 1px solid var(--border);">
                    <td style="padding: 8px;">学术论文</td>
                    <td>${state.stats.arxiv} 篇</td>
                </tr>
                <tr style="border-bottom: 1px solid var(--border);">
                    <td style="padding: 8px;">开源项目</td>
                    <td>${state.stats.github} 个</td>
                </tr>
                <tr style="border-bottom: 1px solid var(--border);">
                    <td style="padding: 8px;">社区讨论</td>
                    <td>${state.stats.hn} 条</td>
                </tr>
            </table>
            
            <h2>⭐ 热门项目</h2>
            ${mockData.github.map(p => `
                <h3><a href="#">${p.title}</a></h3>
                <p>${p.description}</p>
                <p style="color: var(--text-muted); font-size: 12px;">⭐ ${p.stars.toLocaleString()} | 🍴 ${p.forks} | 📝 ${p.language}</p>
            `).join('')}
            
            <h2>📚 重要论文</h2>
            ${mockData.arxiv.map(p => `
                <h3><a href="#">${p.title}</a></h3>
                <p style="color: var(--text-muted);">${p.authors}</p>
                <p>${p.abstract}</p>
            `).join('')}
            
            <hr style="border: none; border-top: 1px solid var(--border); margin: 32px 0;">
            <p style="color: var(--text-muted); font-size: 12px;">由 AI前沿哨兵 自动生成</p>
        </div>
    `;
    
    preview.innerHTML = reportHtml;
    showToast('报告已生成', 'success');
}

// ============================================
// UI更新函数
// ============================================
function updateStats() {
    document.getElementById('statGithub').textContent = state.stats.github;
    document.getElementById('statArxiv').textContent = state.stats.arxiv;
    document.getElementById('statHN').textContent = state.stats.hn;
    document.getElementById('statBlogs').textContent = state.stats.blogs;
}

function updateHotContent(filter = 'all') {
    const container = document.getElementById('hotContent');
    container.innerHTML = '';
    
    let items = [];
    
    if (filter === 'all' || filter === 'projects') {
        mockData.github.forEach(item => {
            items.push({
                type: 'projects',
                title: item.title,
                meta: `⭐ ${item.stars.toLocaleString()} | ${item.language}`,
                score: item.stars
            });
        });
    }
    
    if (filter === 'all' || filter === 'papers') {
        mockData.arxiv.forEach(item => {
            items.push({
                type: 'papers',
                title: item.title,
                meta: item.authors,
                score: 100
            });
        });
    }
    
    if (filter === 'all' || filter === 'discussions') {
        mockData.hackernews.forEach(item => {
            items.push({
                type: 'discussions',
                title: item.title,
                meta: `💬 ${item.comments} 评论`,
                score: item.score
            });
        });
    }
    
    // 按分数排序
    items.sort((a, b) => b.score - a.score);
    
    items.forEach(item => {
        const el = document.createElement('div');
        el.className = 'content-item';
        el.innerHTML = `
            <div>
                <div class="content-item-header">
                    <span class="content-source">${item.type}</span>
                </div>
                <a href="#" class="content-title">${item.title}</a>
                <div class="content-meta">${item.meta}</div>
            </div>
            <div class="content-score">
                <div class="score-value">${item.score}</div>
                <div class="score-label">热度</div>
            </div>
        `;
        container.appendChild(el);
    });
    
    // 过滤标签
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            updateHotContent(tab.dataset.filter);
        });
    });
}

function loadMockData() {
    updateStats();
    updateHotContent();
}

function updateTime() {
    const timeEl = document.getElementById('currentTime');
    if (timeEl) {
        const now = new Date();
        timeEl.textContent = now.toLocaleString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

function addLog(message, status = 'pending') {
    const logList = document.getElementById('logList');
    const emptyLog = logList.querySelector('.log-empty');
    if (emptyLog) emptyLog.remove();
    
    const log = document.createElement('div');
    log.className = 'log-item';
    
    const now = new Date();
    const time = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    
    log.innerHTML = `
        <span class="log-time">${time}</span>
        <span class="log-message">${message}</span>
        <span class="log-status ${status}">${status === 'pending' ? '进行中' : status === 'success' ? '完成' : '错误'}</span>
    `;
    
    logList.insertBefore(log, logList.firstChild);
    
    // 保持最多20条
    while (logList.children.length > 20) {
        logList.removeChild(logList.lastChild);
    }
    
    state.logs.unshift({ time: now.toISOString(), message, status });
}

function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = show ? 'flex' : 'none';
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    container.appendChild(toast);
    
    // 动画
    requestAnimationFrame(() => {
        toast.classList.add('show');
    });
    
    // 自动移除
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// ============================================
// 辅助函数
// ============================================
function getSourceById(id) {
    return builtInSources.find(s => s.id === id) || state.sources.find(s => s.id === id);
}
