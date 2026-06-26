// 获取页面内容的脚本
(function() {
    var result = {
        title: document.title,
        description: '',
        body_length: 0,
        first_paragraph: ''
    };
    
    // 获取 meta 描述
    var metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
        result.description = metaDesc.content;
    }
    
    // 如果没有 meta 描述，尝试 og 描述
    if (!result.description) {
        var ogDesc = document.querySelector('meta[property="og:description"]');
        if (ogDesc) {
            result.description = ogDesc.content;
        }
    }
    
    // 获取正文长度
    result.body_length = document.body.innerText.length;
    
    // 尝试获取第一段有意义的文字
    var selectors = [
        'article',
        '.article-content',
        '.post-content',
        '.entry-content',
        '.content',
        'main',
        '#content'
    ];
    
    var content = '';
    for (var i = 0; i < selectors.length; i++) {
        var elem = document.querySelector(selectors[i]);
        if (elem) {
            var text = elem.innerText || '';
            if (text.length > 100) {
                content = text;
                break;
            }
        }
    }
    
    // 如果没有找到，使用 body
    if (!content) {
        content = document.body.innerText;
    }
    
    // 分割成段落，获取第一段有意义的
    var paragraphs = content.split(/[\n\r]+/);
    for (var i = 0; i < paragraphs.length; i++) {
        var p = paragraphs[i].trim();
        // 跳过太短或太长的
        if (p.length > 30 && p.length < 400) {
            // 跳过看起来像导航的
            if (p.indexOf('登录') === -1 && p.indexOf('注册') === -1) {
                result.first_paragraph = p;
                break;
            }
        }
    }
    
    return JSON.stringify(result);
})();