/**
 * Internationalization (i18n) Module
 * Multi-language support for Agent Dashboard
 */

const I18N = {
    // 当前语言
    currentLang: 'zh',
    
    // 支持的语言
    supportedLangs: ['zh', 'en'],
    
    // 翻译字典
    translations: {
        zh: {
            // 通用
            'app.title': 'Agent Dashboard',
            'app.subtitle': '实时监控 Agent 状态与 Token 使用情况',
            'loading': '加载中...',
            'cancel': '取消',
            'save': '保存',
            'create': '创建',
            'close': '关闭',
            'confirm': '确认',
            'delete': '删除',
            'edit': '编辑',
            'error': '错误',
            'success': '成功',
            
            // 导航和按钮
            'nav.manageSubagents': '调度管理',
            'nav.createAgent': '新建 Agent',
            'nav.settings': '设置',
            'nav.toggleSidebar': '切换详情面板',
            
            // 视图切换
            'view.grid': '卡片视图',
            'view.gridHorizontal': '横向卡片',
            'view.list': '列表视图',
            
            // 侧边栏
            'sidebar.title': '📊 Agent 详情',
            'sidebar.emptyHint': '点击 Agent 卡片查看详情',
            'sidebar.close': '✕',
            
            // 排序提示
            'sort.hint': '拖动卡片左上角的手柄可以调整排序',
            
            // 子 Agent 管理
            'subagents.title': '🔀 子 Agent 调度管理',
            'subagents.dispatcherLabel': '选择调度者 Agent（主 Agent）',
            'subagents.selectPlaceholder': '请选择...',
            'subagents.hint': '被选中的 Agent 可以调度下面配置的子 Agent',
            'subagents.maxConcurrent': '最大并发数',
            'subagents.allowedList': '允许的子 Agent 列表',
            'subagents.checkHint': '勾选允许被调度的 Agent',
            'subagents.saveConfig': '保存配置',
            
            // 技能管理
            'skills.title': '🛠️ Agent 技能管理',
            'skills.detailTitle': '技能详情',
            'skills.enabled': '已启用',
            'skills.available': '可用技能',
            'skills.emptyEnabled': '暂无已启用的技能',
            'skills.emptyAvailable': '所有技能已启用',
            'skills.switchToAvailable': '切换到"可用技能"标签添加技能',
            'skills.allEnabled': '该 Agent 已启用所有可用技能',
            'skills.builtin': '内置',
            'skills.custom': '自定义',
            'skills.enableHint': '点击启用',
            'skills.disableHint': '点击禁用',
            
            // 会话详情
            'session.title': '会话详情',
            
            // 创建 Agent
            'create.title': '➕ 创建新 Agent',
            'create.agentId': 'Agent ID',
            'create.agentIdHint': '唯一标识，创建后不可修改',
            'create.agentIdPlaceholder': '如: my-assistant',
            'create.agentIdPattern': '只允许小写字母、数字、连字符和下划线',
            'create.displayName': '显示名称',
            'create.displayNamePlaceholder': '如: 我的小助手',
            'create.role': '角色',
            'create.rolePlaceholder': '如: 代码助手',
            'create.emoji': 'Emoji 图标',
            'create.colorTheme': '颜色主题',
            'create.color.cyan': '青色 (Cyan)',
            'create.color.main': '蓝紫 (Main)',
            'create.color.coder': '青蓝 (Coder)',
            'create.color.brainstorm': '橙粉 (Brainstorm)',
            'create.color.writer': '绿青 (Writer)',
            'create.color.investor': '绿橙 (Investor)',
            'create.modelProvider': '模型提供商',
            'create.loading': '加载中...',
            'create.selectModel': '选择模型',
            'create.selectProviderFirst': '请先选择提供商',
            'create.description': '描述',
            'create.descriptionPlaceholder': '描述这个 Agent 的用途...',
            'create.systemPrompt': '系统提示词 (System Prompt)',
            'create.systemPromptPlaceholder': '设置 Agent 的系统角色和行为...',
            'create.createButton': '创建 Agent',
            
            // 设置
            'settings.title': '⚙️ Dashboard 设置',
            'settings.dashboardName': 'Dashboard 名称',
            'settings.subtitle': '副标题',
            'settings.subtitlePlaceholder': '实时监控 Agent 状态',
            'settings.refreshInterval': '自动刷新间隔 (秒)',
            'settings.showCost': '显示费用估算',
            'settings.tokenCost': 'Token 成本配置 (元/百万tokens)',
            'settings.inputPrice': '输入 Token 价格',
            'settings.outputPrice': '输出 Token 价格',
            'settings.cachePrice': '缓存 Token 价格',
            'settings.saveButton': '保存设置',
            
            // 头像上传
            'avatar.title': '📷 更换头像',
            'avatar.uploadHint': '点击或拖拽图片到此处',
            'avatar.formatHint': '支持 PNG, JPG, GIF, WebP 格式，最大 5MB',
            'avatar.uploadButton': '上传头像',
            
            // 天气
            'weather.loading': '🌤️ 获取天气中...',
            'weather.error': '🌡️ --',
            'weather.local': '本地',
            
            // 日期时间
            'datetime.weekdays': ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'],
            'datetime.year': '年',
            'datetime.month': '月',
            'datetime.day': '日',
            
            // 状态
            'status.running': '运行中',
            'status.idle': '空闲',
            'status.active': '活跃',
            
            // Token 统计
            'token.total': '总计',
            'token.input': '输入',
            'token.output': '输出',
            'token.cache': '缓存',
            'token.cost': '费用',
            'token.sessions': '会话',
            
            // 通知
            'notify.agentCreated': 'Agent 创建成功',
            'notify.agentDeleted': 'Agent 已删除',
            'notify.settingsSaved': '设置已保存',
            'notify.error': '操作失败',
        },
        en: {
            // General
            'app.title': 'Agent Dashboard',
            'app.subtitle': 'Real-time Agent Status & Token Usage Monitor',
            'loading': 'Loading...',
            'cancel': 'Cancel',
            'save': 'Save',
            'create': 'Create',
            'close': 'Close',
            'confirm': 'Confirm',
            'delete': 'Delete',
            'edit': 'Edit',
            'error': 'Error',
            'success': 'Success',
            
            // Navigation
            'nav.manageSubagents': 'Manage Subagents',
            'nav.createAgent': 'Create Agent',
            'nav.settings': 'Settings',
            'nav.toggleSidebar': 'Toggle Details Panel',
            
            // Views
            'view.grid': 'Grid View',
            'view.gridHorizontal': 'Horizontal Grid',
            'view.list': 'List View',
            
            // Sidebar
            'sidebar.title': '📊 Agent Details',
            'sidebar.emptyHint': 'Click an Agent card to view details',
            'sidebar.close': '✕',
            
            // Sort hint
            'sort.hint': 'Drag the handle at top-left to reorder cards',
            
            // Subagents
            'subagents.title': '🔀 Subagent Dispatch Management',
            'subagents.dispatcherLabel': 'Select Dispatcher Agent (Master)',
            'subagents.selectPlaceholder': 'Please select...',
            'subagents.hint': 'Selected agent can dispatch the configured subagents',
            'subagents.maxConcurrent': 'Max Concurrent',
            'subagents.allowedList': 'Allowed Subagents List',
            'subagents.checkHint': 'Check to allow dispatching',
            'subagents.saveConfig': 'Save Configuration',
            
            // Skills
            'skills.title': '🛠️ Agent Skills Management',
            'skills.detailTitle': 'Skill Details',
            'skills.enabled': 'Enabled',
            'skills.available': 'Available Skills',
            'skills.emptyEnabled': 'No enabled skills yet',
            'skills.emptyAvailable': 'All skills are enabled',
            'skills.switchToAvailable': 'Switch to "Available Skills" tab to add',
            'skills.allEnabled': 'This Agent has all available skills enabled',
            'skills.builtin': 'Built-in',
            'skills.custom': 'Custom',
            'skills.enableHint': 'Click to enable',
            'skills.disableHint': 'Click to disable',
            
            // Session
            'session.title': 'Session Details',
            
            // Create Agent
            'create.title': '➕ Create New Agent',
            'create.agentId': 'Agent ID',
            'create.agentIdHint': 'Unique identifier, cannot be changed after creation',
            'create.agentIdPlaceholder': 'e.g., my-assistant',
            'create.agentIdPattern': 'Only lowercase letters, numbers, hyphens and underscores',
            'create.displayName': 'Display Name',
            'create.displayNamePlaceholder': 'e.g., My Assistant',
            'create.role': 'Role',
            'create.rolePlaceholder': 'e.g., Code Assistant',
            'create.emoji': 'Emoji Icon',
            'create.colorTheme': 'Color Theme',
            'create.color.cyan': 'Cyan',
            'create.color.main': 'Blue-Purple',
            'create.color.coder': 'Cyan-Blue',
            'create.color.brainstorm': 'Orange-Pink',
            'create.color.writer': 'Green-Cyan',
            'create.color.investor': 'Green-Orange',
            'create.modelProvider': 'Model Provider',
            'create.loading': 'Loading...',
            'create.selectModel': 'Select Model',
            'create.selectProviderFirst': 'Please select provider first',
            'create.description': 'Description',
            'create.descriptionPlaceholder': 'Describe the purpose of this Agent...',
            'create.systemPrompt': 'System Prompt',
            'create.systemPromptPlaceholder': 'Set the system role and behavior...',
            'create.createButton': 'Create Agent',
            
            // Settings
            'settings.title': '⚙️ Dashboard Settings',
            'settings.dashboardName': 'Dashboard Name',
            'settings.subtitle': 'Subtitle',
            'settings.subtitlePlaceholder': 'Real-time Agent status monitoring',
            'settings.refreshInterval': 'Auto-refresh Interval (seconds)',
            'settings.showCost': 'Show Cost Estimates',
            'settings.tokenCost': 'Token Cost Configuration (per million tokens)',
            'settings.inputPrice': 'Input Token Price',
            'settings.outputPrice': 'Output Token Price',
            'settings.cachePrice': 'Cache Token Price',
            'settings.saveButton': 'Save Settings',
            
            // Avatar
            'avatar.title': '📷 Change Avatar',
            'avatar.uploadHint': 'Click or drag image here',
            'avatar.formatHint': 'Supports PNG, JPG, GIF, WebP, max 5MB',
            'avatar.uploadButton': 'Upload Avatar',
            
            // Weather
            'weather.loading': '🌤️ Getting weather...',
            'weather.error': '🌡️ --',
            'weather.local': 'Local',
            
            // DateTime
            'datetime.weekdays': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'datetime.year': '',
            'datetime.month': '/',
            'datetime.day': '',
            
            // Status
            'status.running': 'Running',
            'status.idle': 'Idle',
            'status.active': 'Active',
            
            // Token
            'token.total': 'Total',
            'token.input': 'Input',
            'token.output': 'Output',
            'token.cache': 'Cache',
            'token.cost': 'Cost',
            'token.sessions': 'Sessions',
            
            // Notifications
            'notify.agentCreated': 'Agent created successfully',
            'notify.agentDeleted': 'Agent deleted',
            'notify.settingsSaved': 'Settings saved',
            'notify.error': 'Operation failed',
        }
    },
    
    /**
     * Initialize i18n
     */
    init() {
        // Detect language from browser
        const browserLang = navigator.language || navigator.userLanguage || 'zh';
        const langCode = browserLang.split('-')[0].toLowerCase();
        
        // Check if supported
        if (this.supportedLangs.includes(langCode)) {
            this.currentLang = langCode;
        } else {
            this.currentLang = 'en'; // Default to English for unsupported languages
        }
        
        console.log(`[i18n] Language detected: ${browserLang}, using: ${this.currentLang}`);
    },
    
    /**
     * Get translation by key
     * @param {string} key - Translation key
     * @param {object} params - Optional parameters for interpolation
     * @returns {string} Translated text
     */
    t(key, params = {}) {
        const translation = this.translations[this.currentLang]?.[key] || 
                           this.translations['en']?.[key] || 
                           key;
        
        // Simple interpolation
        if (typeof translation === 'string' && Object.keys(params).length > 0) {
            return translation.replace(/\{\{(\w+)\}\}/g, (match, p1) => params[p1] || match);
        }
        
        return translation;
    },
    
    /**
     * Get array translation (e.g., weekdays)
     * @param {string} key - Translation key
     * @returns {array} Translated array
     */
    tArray(key) {
        return this.translations[this.currentLang]?.[key] || 
               this.translations['en']?.[key] || 
               [];
    },
    
    /**
     * Format date according to current locale
     * @param {Date} date - Date object
     * @returns {string} Formatted date string
     */
    formatDate(date) {
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        const weekdays = this.tArray('datetime.weekdays');
        const weekday = weekdays[date.getDay()] || '';
        
        if (this.currentLang === 'zh') {
            return `${year}${this.t('datetime.year')}${month}${this.t('datetime.month')}${day}${this.t('datetime.day')} ${weekday}`;
        } else {
            return `${year}${this.t('datetime.year')}${month}${this.t('datetime.month')}${day} ${weekday}`;
        }
    },
    
    /**
     * Format time according to current locale
     * @param {Date} date - Date object
     * @returns {string} Formatted time string
     */
    formatTime(date) {
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        return `${hours}:${minutes}:${seconds}`;
    }
};

// Initialize on load
I18N.init();

// Make globally available
window.I18N = I18N;
window.t = (key, params) => I18N.t(key, params);
