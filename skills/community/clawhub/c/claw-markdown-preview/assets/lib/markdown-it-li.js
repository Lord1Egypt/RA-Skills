function makeLiRule(md) {
  return function replaceListItem() {
    md.renderer.rules.list_item_open = function replaceOpen() {
      return "<li><section>";
    };
    md.renderer.rules.list_item_close = function replaceClose() {
      return "</section></li>";
    };
  };
}

function markdownItLiReplacer(md) {
  md.core.ruler.push("replace-li", makeLiRule(md));
}

window.AutoArticle = window.AutoArticle || {};
window.AutoArticle.plugins = window.AutoArticle.plugins || {};
window.AutoArticle.plugins.markdownItLiReplacer = markdownItLiReplacer;