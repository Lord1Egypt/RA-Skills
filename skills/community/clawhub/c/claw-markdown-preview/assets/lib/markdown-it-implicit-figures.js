'use strict';

function implicitFiguresPlugin(md, options) {
  options = options || {};

  function implicitFigures(state) {
    var tabIndex = 1;

    for (var i = 1, l = state.tokens.length; i < (l - 1); ++i) {
      var token = state.tokens[i];

      if (token.type !== 'inline') { continue; }
      if (!token.children || (token.children.length !== 1 && token.children.length !== 3)) { continue; }
      if (token.children.length === 1 && token.children[0].type !== 'image') { continue; }
      if (token.children.length === 3 &&
          (token.children[0].type !== 'link_open' ||
           token.children[1].type !== 'image' ||
           token.children[2].type !== 'link_close')) {
        continue;
      }
      if (i !== 0 && state.tokens[i - 1].type !== 'paragraph_open') { continue; }
      if (i !== (l - 1) && state.tokens[i + 1].type !== 'paragraph_close') { continue; }

      var figure = state.tokens[i - 1];
      figure.type = 'figure_open';
      figure.tag = 'figure';
      state.tokens[i + 1].type = 'figure_close';
      state.tokens[i + 1].tag = 'figure';

      if (options.dataType == true) {
        state.tokens[i - 1].attrPush(['data-type', 'image']);
      }
      var image;

      if (options.link == true && token.children.length === 1) {
        image = token.children[0];
        token.children.unshift(
          new state.Token('link_open', 'a', 1)
        );
        token.children[0].attrPush(['href', image.attrGet('src')]);
        token.children.push(
          new state.Token('link_close', 'a', -1)
        );
      }

      image = token.children.length === 1 ? token.children[0] : token.children[1];

      if (options.figcaption) {
        var captionOptionString = new String(options.figcaption).toLowerCase().trim();

        if (captionOptionString == 'title') {
          var figCaption;
          var captionObj = image.attrs.find(function (k) {
            return k[0] === 'title';
          });

          if (Array.isArray(captionObj)) {
            figCaption = captionObj[1];
          }

          if (figCaption) {
            var captionArray = md.parseInline(figCaption);
            var captionContent = { children: []};

            if (Array.isArray(captionArray) && captionArray.length) {
              captionContent = captionArray[0];
            }

            token.children.push(
              new state.Token('figcaption_open', 'figcaption', 1)
            );
            token.children.push.apply(token.children, captionContent.children);
            token.children.push(
              new state.Token('figcaption_close', 'figcaption', -1)
            );

            if (image.attrs) {
              image.attrs = image.attrs.filter(function (k) {
                return k[0] !== 'title';
              });
            }
          }
        }
        else if (options.figcaption == true || captionOptionString == 'alt') {
          // 过滤掉 undefined/null 的 children，避免输出 <undefined> 标签
          var validChildren = image.children ? image.children.filter(function (c) { return c; }) : [];
          if (validChildren.length) {
            token.children.push(
              new state.Token('figcaption_open', 'figcaption', 1)
            );
            token.children.push.apply(token.children, validChildren);
            token.children.push(
              new state.Token('figcaption_close', 'figcaption', -1)
            );
            if (!options.keepAlt) image.children.length = 0;
          }
        }
      }

      if (options.copyAttrs && image.attrs) {
        var f = options.copyAttrs === true ? '' : options.copyAttrs;
        figure.attrs = image.attrs.filter(function (k) {
          return k[0].match(f);
        });
      }

      if (options.tabindex == true) {
        state.tokens[i - 1].attrPush(['tabindex', tabIndex]);
        tabIndex++;
      }

      if (options.lazyLoading == true) {
        image.attrPush(['loading', 'lazy']);
      }
    }
  }
  md.core.ruler.before('linkify', 'implicit_figures', implicitFigures);
}

window.AutoArticle = window.AutoArticle || {};
window.AutoArticle.plugins = window.AutoArticle.plugins || {};
window.AutoArticle.plugins.markdownitImplicitFigures = implicitFiguresPlugin;