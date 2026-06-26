/**
 * Internationalization (i18n) Module
 * Bilingual support for Chinese (zh-CN) and English (en)
 */

const i18n = {
  // Current language
  currentLang: localStorage.getItem('dashboard-lang') || 'en',

  // Translation dictionary
  translations: {
    'en': {
      // Header
      'title': '📊 Eisenhower Task Dashboard',
      'status_connecting': 'Connecting...',
      'status_live': 'Live',
      'status_offline': 'Offline',

      // Stats bar
      'q1_label': '🔥 Q1 Urgent & Important',
      'q2_label': '💼 Q2 Important Not Urgent',
      'q3_label': '⚡ Q3 Urgent Not Important',
      'q4_label': '🧘 Q4 Not Urgent & Important',
      'customer_label': '🏢 Customer Projects',
      'delegation_label': '👑 Delegation Tasks',
      'maybe_label': '🌱 Maybe List',

      // Navigation tabs
      'tab_matrix': 'Eisenhower Matrix',
      'tab_customers': 'Customer Projects',
      'tab_delegation': 'Delegation',
      'tab_maybe': 'Maybe List',

      // Quadrant section titles
      'q1_title': '🔥 Q1: Urgent & Important',
      'q1_subtitle': 'Do First',
      'q2_title': '💼 Q2: Important Not Urgent',
      'q2_subtitle': 'Schedule',
      'q3_title': '⚡ Q3: Not Important Urgent',
      'q3_subtitle': 'Batch / Delegate',
      'q4_title': '🧘 Q4: Not Urgent & Important',
      'q4_subtitle': 'Delete / Postpone',

      // Customer section
      'customer_title': '🏢 Customer Project List',
      'filter_all': 'All',
      'filter_active': 'Active',
      'filter_blocked': 'Blocked',

      // Delegation section
      'delegation_title': '👑 Delegation Task List',
      'filter_inprogress': 'In Progress',
      'filter_overdue': 'Overdue',
      'assignee_prefix': 'Assignee:',
      'deadline_prefix': 'Due:',
      'deadline_overdue': '⚠️ Overdue:',

      // Maybe section
      'maybe_title': '🌱 Maybe List',
      'maybe_desc': 'Ideas and inspirations for future consideration, not yet in the matrix',

      // Footer
      'last_updated': 'Last updated:',

      // Empty states
      'empty_tasks': 'No tasks',
      'empty_customer': 'No customer projects',
      'empty_delegation': 'No delegation tasks',
      'empty_maybe': 'No future plans',
      'empty_filtered': 'No matching items',

      // Task meta
      'created_prefix': 'Created:',
      'updated_prefix': 'Updated:',
      'reviewed_prefix': 'Reviewed:',
      'blocked_badge': '🚫 Blocked',
      'type_prefix': 'Type:',
      'priority_prefix': 'Priority:',
      'description': 'Description',
      'subtasks': 'Subtasks',
      'tags': 'Tags',
      'assignee_prefix': 'Assignee:',

      // Language switcher
      'language': 'Language',
      'lang_en': 'English',
      'lang_zh': '中文',

      // Status labels
      'status_active': 'Active',
      'status_blocked': 'Blocked',
      'status_pending': 'Pending',
      'status_in_progress': 'In Progress',
      'status_todo': 'To Do',

      // Drag and drop
      'drag_to_reorder': 'Drag to reorder',

      // Copy menu
      'copy_task_to': 'Copy Task to...',
      'copy_project_to': 'Copy Project to...',
      'quadrants': 'Four Quadrants',
      'delegation': 'Delegation',
      'delegation_list': 'Delegation List',
      'customer_projects': 'Customer Projects',
      'cancel': 'Cancel',

      // Move menu
      'move_task_to': 'Move Task to...',
      'target_list': 'Target List',
      'maybe_list': 'Maybe List'
    },
    'zh-CN': {
      // Header
      'title': '📊 Eisenhower Task Dashboard',
      'status_connecting': '连接中...',
      'status_live': '实时连接',
      'status_offline': '离线',

      // Stats bar
      'q1_label': '🔥 Q1 重要+紧急',
      'q2_label': '💼 Q2 重要不紧急',
      'q3_label': '⚡ Q3 不重要紧急',
      'q4_label': '🧘 Q4 不重要不紧急',
      'customer_label': '🏢 客户项目',
      'delegation_label': '👑 委派任务',
      'maybe_label': '🌱 未来清单',

      // Navigation tabs
      'tab_matrix': '四象限矩阵',
      'tab_customers': '客户项目',
      'tab_delegation': '委派任务',
      'tab_maybe': '未来清单',

      // Quadrant section titles
      'q1_title': '🔥 Q1: 重要+紧急',
      'q1_subtitle': '立即执行',
      'q2_title': '💼 Q2: 重要不紧急',
      'q2_subtitle': '计划执行',
      'q3_title': '⚡ Q3: 不重要紧急',
      'q3_subtitle': '批量/委派',
      'q4_title': '🧘 Q4: 不重要不紧急',
      'q4_subtitle': '推迟/删除',

      // Customer section
      'customer_title': '🏢 客户项目清单',
      'filter_all': '全部',
      'filter_active': '进行中',
      'filter_blocked': '阻塞中',

      // Delegation section
      'delegation_title': '👑 委派任务清单',
      'filter_inprogress': '进行中',
      'filter_overdue': '已逾期',
      'assignee_prefix': '责任人:',
      'deadline_prefix': '截止:',
      'deadline_overdue': '⚠️ 已逾期:',

      // Maybe section
      'maybe_title': '🌱 未来清单 (Maybe List)',
      'maybe_desc': '可能以后做的想法和灵感，暂不放入四象限',

      // Footer
      'last_updated': '最后更新:',

      // Empty states
      'empty_tasks': '暂无任务',
      'empty_customer': '暂无客户项目',
      'empty_delegation': '暂无委派任务',
      'empty_maybe': '暂无未来计划',
      'empty_filtered': '没有符合条件的项目',

      // Task meta
      'created_prefix': '创建于:',
      'updated_prefix': '更新于:',
      'reviewed_prefix': 'Reviewed:',
      'blocked_badge': '🚫 阻塞',
      'type_prefix': 'Type:',
      'priority_prefix': 'Priority:',
      'description': '描述',
      'subtasks': '子任务',
      'tags': '标签',
      'assignee_prefix': '责任人:',

      // Language switcher
      'language': '语言',
      'lang_en': 'English',
      'lang_zh': '中文',

      // Status labels
      'status_active': 'Active',
      'status_blocked': 'Blocked',
      'status_pending': 'Pending',
      'status_in_progress': '进行中',
      'status_todo': '待开始',

      // Drag and drop
      'drag_to_reorder': '拖拽排序',

      // Copy menu
      'copy_task_to': '复制任务到...',
      'copy_project_to': '复制项目到...',
      'quadrants': '四象限',
      'delegation': '委派',
      'delegation_list': '委派清单',
      'customer_projects': '客户项目',
      'cancel': '取消',

      // Move menu
      'move_task_to': '移动任务到...',
      'target_list': '目标清单',
      'maybe_list': '未来清单'
    }
  },



  /**
   * Get translation for a key
   */
  t(key) {
    const lang = this.currentLang;
    if (this.translations[lang] && this.translations[lang][key]) {
      return this.translations[lang][key];
    }
    // Fallback to English
    if (this.translations['en'][key]) {
      return this.translations['en'][key];
    }
    // Return key if not found
    return key;
  },

  /**
   * Set language and persist to localStorage
   */
  setLanguage(lang) {
    if (this.translations[lang]) {
      this.currentLang = lang;
      localStorage.setItem('dashboard-lang', lang);
      this.updatePageLanguage();
      return true;
    }
    return false;
  },

  /**
   * Get current language
   */
  getLanguage() {
    return this.currentLang;
  },

  /**
   * Update all elements with data-i18n attribute
   */
  updatePageLanguage() {
    // Update data-i18n elements
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      const translation = this.t(key);

      // Check if element has child elements (preserve structure)
      if (el.children.length > 0 && el.textContent.trim() !== translation) {
        // Update only text nodes, preserve child elements
        const textNodes = Array.from(el.childNodes).filter(
          node => node.nodeType === Node.TEXT_NODE && node.textContent.trim()
        );
        if (textNodes.length > 0) {
          textNodes.forEach(node => {
            node.textContent = translation;
          });
        } else {
          // If no text nodes found, check for value attribute (inputs)
          if (el.hasAttribute('value')) {
            el.setAttribute('value', translation);
          } else if (el.hasAttribute('placeholder')) {
            el.setAttribute('placeholder', translation);
          }
        }
      } else {
        // Simple text content update
        el.textContent = translation;
      }
    });

    // Update data-i18n-placeholder elements
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const key = el.getAttribute('data-i18n-placeholder');
      el.setAttribute('placeholder', this.t(key));
    });

    // Update data-i18n-title elements (tooltips)
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
      const key = el.getAttribute('data-i18n-title');
      el.setAttribute('title', this.t(key));
    });

    // Update HTML lang attribute
    document.documentElement.lang = this.currentLang === 'zh-CN' ? 'zh-CN' : 'en';
  },

  /**
   * Initialize language on page load
   */
  init() {
    this.updatePageLanguage();
  }
};

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  i18n.init();
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = i18n;
}
