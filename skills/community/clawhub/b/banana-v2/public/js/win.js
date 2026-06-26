/**
 * Nano Banana V2 - 弹窗管理器
 * 依赖: jQuery
 */

// 全局翻译函数 - 供组件使用
// 如果主窗口有 t 函数则使用，否则返回 key 或默认值
function t(key, defaultValue) {
    if (typeof window.parent !== 'undefined' && typeof window.parent.t === 'function') {
        return window.parent.t(key);
    }
    if (typeof window.t === 'function') {
        return window.t(key);
    }
    // 返回默认值或 key
    return defaultValue || key;
}

// 弹窗管理器
const WinManager = {
    // 存储所有打开的窗口
    windows: {},
    // 窗口层级计数器
    zIndex: 1000,
    
    /**
     * 打开一个弹窗
     * @param {string} id - 窗口唯一ID
     * @param {string} title - 窗口标题
     * @param {string} url - 组件URL (相对于 /components/)
     * @param {number} width - 窗口宽度，默认500
     * @param {string} bg - 窗口图标背景色
     * @returns {jQuery} 窗口jQuery对象
     */
    open: function(id, title, url, width = 500, bg = '') {
        // 如果窗口已存在，直接显示并置顶
        if (this.windows[id]) {
            this.focus(id);
            return this.windows[id].element;
        }
        
        const self = this;
        this.zIndex++;
        
        // 创建窗口结构
        const $win = $(`
            <div class="win-modal" id="win-${id}" style="z-index: ${this.zIndex};">
                <div class="win-overlay"></div>
                <div class="win-container" style="width: ${width}px;">
                    <div class="win-header">
                        
                        <h3 class="win-title">${title}</h3>
                        <button class="win-close" data-win="${id}">×</button>
                    </div>
                    <div class="win-body">
                        <div class="win-loading">
                            <div class="win-spinner"></div>
                            <span>加载中...</span>
                        </div>
                    </div>
                </div>
            </div>
        `);
        
        // 添加到页面
        $('body').append($win);
        
        // 存储窗口信息
        this.windows[id] = {
            element: $win,
            title: title,
            url: url
        };
        
        // 绑定关闭事件
        $win.find('.win-close, .win-overlay').on('click', function() {
            self.close(id);
        });
        
        // 点击窗口置顶
        $win.on('mousedown', function() {
            self.focus(id);
        });
        
        // AJAX 加载组件内容
        if (url) {
            $.ajax({
                url: `/components/${url}`,
                type: 'GET',
                success: function(html) {
                    $win.find('.win-body').html(html);
                    // 执行组件内的脚本
                    $win.find('.win-body script').each(function() {
                        eval($(this).text());
                    });
                },
                error: function(xhr, status, error) {
                    $win.find('.win-body').html(`
                        <div class="win-error">
                            <span>⚠️</span>
                            <p>加载失败: ${error}</p>
                        </div>
                    `);
                }
            });
        }
        
        // 显示动画
        setTimeout(() => $win.addClass('win-show'), 10);
        
        return $win;
    },
    
    /**
     * 关闭窗口
     * @param {string} id - 窗口ID
     */
    close: function(id) {
        if (this.windows[id]) {
            const $win = this.windows[id].element;
            $win.removeClass('win-show');
            setTimeout(() => {
                $win.remove();
                delete this.windows[id];
            }, 300);
        }
    },
    
    /**
     * 关闭所有窗口
     */
    closeAll: function() {
        for (let id in this.windows) {
            this.close(id);
        }
    },
    
    /**
     * 窗口置顶
     * @param {string} id - 窗口ID
     */
    focus: function(id) {
        if (this.windows[id]) {
            this.zIndex++;
            this.windows[id].element.css('z-index', this.zIndex);
        }
    },
    
    /**
     * 获取窗口
     * @param {string} id - 窗口ID
     * @returns {jQuery|null}
     */
    get: function(id) {
        return this.windows[id] ? this.windows[id].element : null;
    },
    
    /**
     * 设置窗口标题
     * @param {string} id - 窗口ID
     * @param {string} title - 新标题
     */
    setTitle: function(id, title) {
        if (this.windows[id]) {
            this.windows[id].element.find('.win-title').text(title);
        }
    },
    
    /**
     * 设置窗口内容
     * @param {string} id - 窗口ID
     * @param {string} content - HTML内容
     */
    setContent: function(id, content) {
        if (this.windows[id]) {
            this.windows[id].element.find('.win-body').html(content);
        }
    }
};

// 快捷函数
function win(id, title, url, width = 500, bg = '') {
    return WinManager.open(id, title, url, width, bg);
}

// 关闭窗口
function winClose(id) {
    WinManager.close(id);
}

// 关闭所有窗口
function winCloseAll() {
    WinManager.closeAll();
}
