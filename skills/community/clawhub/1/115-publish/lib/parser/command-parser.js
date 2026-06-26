/**
 * 快捷命令解析器
 * 
 * 解析用户输入，支持多种命令格式：
 * - /115 [命令] [参数]
 * - 数字选择 (1-9)
 * - 自然语言命令
 * - 快捷词
 */

class CommandParser {
  constructor() {
    // 快捷词映射
    this.shortcuts = {
      // 容量相关
      '容量': 'status',
      '空间': 'status',
      '剩余空间': 'status',
      '存储空间': 'status',
      
      // 文件浏览
      '文件': 'files',
      '文件列表': 'files',
      '查看文件': 'files',
      '浏览': 'files',
      
      // 搜索
      '搜索': 'search',
      '查找': 'search',
      '找': 'search',
      
      // 登录
      '登录': 'login',
      '扫码登录': 'login',
      '115 登录': 'login',
      
      // 转存
      '转存': 'transfer',
      '保存': 'transfer',
      
      // 下载
      '下载': 'download',
      '离线下载': 'download',
      '下载任务': 'download',
      
      // 分享
      '分享': 'share',
      '我的分享': 'shareList',
      '分享列表': 'shareList',
      
      // 整理
      '整理': 'organize',
      '分类整理': 'organize',
      '智能整理': 'organize',
      
      // 清理
      '清理': 'clean',
      '清理建议': 'clean',
      '优化空间': 'clean',
      
      // 操作
      '返回': 'back',
      '上级': 'back',
      '上一页': 'back',
      '打开': 'open',
      '进入': 'open',
      '删除': 'delete',
      '重命名': 'rename',
      '移动': 'move',
      '复制': 'copy',
      '新建': 'create',
      '新建文件夹': 'createFolder',
    };

    // 命令别名
    this.aliases = {
      'ls': 'files',
      'list': 'files',
      'cd': 'open',
      'back': 'back',
      'rm': 'delete',
      'mv': 'move',
      'cp': 'copy',
      'mkdir': 'create_folder',
    };
  }

  /**
   * 解析用户输入
   * @param {string} input - 用户输入
   * @param {Object} context - 当前上下文（可选）
   * @returns {Object} 解析结果
   */
  parse(input, context = null) {
    if (!input || typeof input !== 'string') {
      return this._createResult('unknown', null, input);
    }

    const trimmed = input.trim();

    // 1. 检查数字选择
    if (/^[1-9]$/.test(trimmed)) {
      return this._createResult('select', { index: parseInt(trimmed) }, input);
    }

    // 2. 检查 /115 命令格式
    if (trimmed.startsWith('/115') || trimmed.startsWith('/115-skills')) {
      return this._parseSlashCommand(trimmed);
    }

    // 3. 检查 115 分享链接
    if (trimmed.includes('115.com/s/')) {
      return this._parseShareLink(trimmed);
    }

    // 4. 检查磁力链接
    if (trimmed.startsWith('magnet:')) {
      return this._createResult('download', { type: 'magnet', url: trimmed }, input);
    }

    // 5. 检查 HTTP 链接
    if (trimmed.startsWith('http://') || trimmed.startsWith('https://')) {
      return this._createResult('download', { type: 'http', url: trimmed }, input);
    }

    // 6. 解析自然语言命令
    return this._parseNaturalLanguage(trimmed, context);
  }

  /**
   * 解析斜杠命令
   * @param {string} input - 用户输入
   * @returns {Object} 解析结果
   */
  _parseSlashCommand(input) {
    // 移除 /115 或 /115-skills 前缀
    const parts = input.replace(/^\/115(-skills)?\s*/, '').trim().split(/\s+/);
    const command = parts[0]?.toLowerCase();
    const args = parts.slice(1);

    // 检查别名
    let normalizedCommand = this.aliases[command] || command;
    
    // 检查是否是中文快捷词，需要转换
    if (this.shortcuts[command]) {
      normalizedCommand = this.shortcuts[command];
    }

    return this._createResult(normalizedCommand, { args }, input);
  }

  /**
   * 解析分享链接
   * @param {string} input - 用户输入
   * @returns {Object} 解析结果
   */
  _parseShareLink(input) {
    // 提取分享码
    const match = input.match(/115\.com\/s\/([a-zA-Z0-9]+)/);
    const shareCode = match ? match[1] : null;

    // 提取密码（支持多种格式：密码：xxx 密码:xxx 密码 xxx）
    const passwordMatch = input.match(/密码\s*[：:]\s*([a-zA-Z0-9]+)/i);
    const password = passwordMatch ? passwordMatch[1] : null;

    return this._createResult('transfer', {
      type: 'share',
      shareCode,
      password,
      url: input
    }, input);
  }

  /**
   * 解析自然语言命令
   * @param {string} input - 用户输入
   * @param {Object} context - 当前上下文
   * @returns {Object} 解析结果
   */
  _parseNaturalLanguage(input, context) {
    // 尝试匹配快捷词（优先匹配长关键词）
    const sortedShortcuts = Object.entries(this.shortcuts).sort(
      (a, b) => b[0].length - a[0].length
    );
    
    for (const [keyword, command] of sortedShortcuts) {
      if (input === keyword || input.startsWith(keyword + ' ') || input.startsWith(keyword)) {
        // 提取参数
        const parts = input.split(keyword);
        const param = parts[1]?.trim() || null;

        // 特殊处理
        if (command === 'search' && param) {
          return this._createResult('search', { keyword: param }, input);
        }

        if (command === 'open' && param) {
          return this._createResult('open', { name: param }, input);
        }

        if (command === 'status') {
          return this._createResult('status', {}, input);
        }

        return this._createResult(command, { param }, input);
      }
    }

    // 检查是否是文件名（用于打开）
    if (context?.selectedFiles?.length > 0) {
      return this._createResult('open', { name: input }, input);
    }

    // 未知命令
    return this._createResult('unknown', null, input);
  }

  /**
   * 创建解析结果
   * @param {string} command - 命令
   * @param {Object} params - 参数
   * @param {string} originalInput - 原始输入
   * @returns {Object} 解析结果
   */
  _createResult(command, params = {}, originalInput = '') {
    return {
      command,
      params,
      originalInput,
      timestamp: Date.now()
    };
  }

  /**
   * 注册快捷词
   * @param {string} keyword - 快捷词
   * @param {string} command - 对应命令
   */
  registerShortcut(keyword, command) {
    this.shortcuts[keyword.toLowerCase()] = command;
  }

  /**
   * 注册别名
   * @param {string} alias - 别名
   * @param {string} command - 对应命令
   */
  registerAlias(alias, command) {
    this.aliases[alias.toLowerCase()] = command;
  }

  /**
   * 获取所有快捷词
   * @returns {Object} 快捷词映射
   */
  getShortcuts() {
    return { ...this.shortcuts };
  }

  /**
   * 获取所有别名
   * @returns {Object} 别名映射
   */
  getAliases() {
    return { ...this.aliases };
  }

  /**
   * 验证命令是否有效
   * @param {string} command - 命令
   * @returns {boolean}
   */
  isValidCommand(command) {
    const validCommands = [
      'login', 'files', 'search', 'transfer', 'download',
      'organize', 'status', 'clean', 'back', 'open',
      'delete', 'rename', 'move', 'copy', 'create',
      'createFolder', 'share', 'shareList', 'select', 'unknown'
    ];
    return validCommands.includes(command);
  }

  /**
   * 获取命令帮助
   * @param {string} command - 命令
   * @returns {string} 帮助信息
   */
  getHelp(command) {
    const helpMap = {
      'login': '登录 115 - 扫码登录到 115 网盘',
      'files': '查看文件 - 浏览当前目录文件列表',
      'search [关键词]': '搜索 xxx - 搜索文件',
      'transfer [链接]': '转存 115.com/s/xxx - 转存分享文件',
      'download [链接]': '下载 xxx - 添加离线下载任务',
      'organize': '整理文件 - 智能分类整理文件',
      'status': '容量 - 查看存储空间使用情况',
      'clean': '清理建议 - 获取空间优化建议',
      'back': '返回 - 返回上一级目录',
      'open [名称]': '打开 xxx - 进入目录或打开文件',
      'delete': '删除 - 删除选中的文件',
      'rename': '重命名 - 重命名文件',
      'move': '移动 - 移动文件到其他目录',
      'copy': '复制 - 复制文件',
      'create_folder [名称]': '新建文件夹 - 创建新目录',
      'share': '分享 - 分享当前选中的文件',
      'share_list': '我的分享 - 查看分享列表',
    };

    return helpMap[command] || '未知命令';
  }

  /**
   * 获取所有可用命令
   * @returns {Array<string>}
   */
  getAvailableCommands() {
    return [
      'login', 'files', 'search', 'transfer', 'download',
      'organize', 'status', 'clean', 'back', 'open',
      'delete', 'rename', 'move', 'copy', 'create',
      'create_folder', 'share', 'share_list'
    ];
  }
}

module.exports = CommandParser;
