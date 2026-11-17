function makeUrlSpanRule(md) {
  return function addUrlSpan() {
    md.renderer.rules.link_open = function(tokens, idx, options, env, self) {
      const hrefIndex = tokens[idx].attrIndex('href');
      const hrefValue = tokens[idx].attrs[hrefIndex][1];
      const description = tokens[idx + 1].content;
      const linkContent = `<a href="${hrefValue}"><span>`;
      return linkContent;
    };

    md.renderer.rules.link_close = function replaceClose() {
      return '</span></a>';
    };
  };
}

function markdownItUrlAddSpan(md) {
  md.core.ruler.push("add-url-span", makeUrlSpanRule(md));
}

window.AutoArticle = window.AutoArticle || {};
window.AutoArticle.plugins = window.AutoArticle.plugins || {};
window.AutoArticle.plugins.markdownItUrlAddSpan = markdownItUrlAddSpan;