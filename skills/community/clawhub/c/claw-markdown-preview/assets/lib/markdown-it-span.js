function slugify(s, md) {
  var spaceRegex = new RegExp(md.utils.lib.ucmicro.Z.source, "g");
  return encodeURIComponent(s.replace(spaceRegex, ""));
}

function makeHeadingSpanRule(md, options) {
  return function addHeadingAnchors(state) {
    for (var i = 0; i < state.tokens.length - 1; i++) {
      if (state.tokens[i].type !== "heading_open" || state.tokens[i + 1].type !== "inline") {
        continue;
      }

      var headingInlineToken = state.tokens[i + 1];

      if (!headingInlineToken.content) {
        continue;
      }

      if (options.addHeadingSpan) {
        var spanTokenPre = new state.Token("html_inline", "", 0);
        spanTokenPre.content = `<span class="prefix"></span><span class="content">`;
        if (!headingInlineToken.children) {
          headingInlineToken.children = [];
        }
        headingInlineToken.children.unshift(spanTokenPre);
        var spanTokenPost = new state.Token("html_inline", "", 0);
        spanTokenPost.content = `</span><span class="suffix"></span>`;
        headingInlineToken.children.push(spanTokenPost);
      }

      i += 2;
    }
  };
}

function markdownItSpan(md, opts) {
  var defaults = {
    anchorClass: "markdown-it-headingspan",
    addHeadingSpan: true,
    slugify: slugify,
  };
  var options = md.utils.assign(defaults, opts);
  md.core.ruler.push("heading_span", makeHeadingSpanRule(md, options));
}

window.AutoArticle = window.AutoArticle || {};
window.AutoArticle.plugins = window.AutoArticle.plugins || {};
window.AutoArticle.plugins.markdownitSpan = markdownItSpan;