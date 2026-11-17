// markdown-it-linkfoot: 将链接转为脚注形式（微信文章中链接会变色，转为脚注可保持样式一致）
// 基于 Markdown2Html 项目的 markdown-it-linkfoot.js 适配浏览器环境

function renderFootnoteAnchorName(tokens, idx, options, env) {
  var n = Number(tokens[idx].meta.id + 1).toString();
  var prefix = "";

  if (typeof env.docId === "string") {
    prefix = "-" + env.docId + "-";
  }

  return prefix + n;
}

function renderFootnoteCaption(tokens, idx) {
  var n = Number(tokens[idx].meta.id + 1).toString();

  if (tokens[idx].meta.subId > 0) {
    n += ":" + tokens[idx].meta.subId;
  }

  return "[" + n + "]";
}

function renderFootnoteWord(tokens, idx) {
  return '<span class="footnote-word">' + tokens[idx].content + "</span>";
}

function renderFootnoteRef(tokens, idx, options, env, slf) {
  var caption = slf.rules.footnote_caption(tokens, idx, options, env, slf);
  return '<sup class="footnote-ref">' + caption + "</sup>";
}

function renderFootnoteBlockOpen() {
  return '<h3 class="footnotes-sep"></h3>\n<section class="footnotes">\n';
}

function renderFootnoteBlockClose() {
  return "</section>\n";
}

function renderFootnoteOpen(tokens, idx, options, env, slf) {
  var id = slf.rules.footnote_anchor_name(tokens, idx, options, env, slf);

  if (tokens[idx].meta.subId > 0) {
    id += ":" + tokens[idx].meta.subId;
  }

  return '<span id="fn' + id + '" class="footnote-item"><span class="footnote-num">[' + id + "] </span>";
}

function renderFootnoteClose() {
  return "</span>\n";
}

function isSpace(code) {
  switch (code) {
    case 0x09:
    case 0x20:
      return true;
    default:
  }
  return false;
}

function normalizeReference(str) {
  return str
    .trim()
    .replace(/\s+/g, " ")
    .toUpperCase();
}

function linkFoot(state, silent) {
  var attrs,
    code,
    label,
    pos,
    res,
    ref,
    title,
    token,
    href = "",
    start = state.pos,
    footnoteContent,
    parseReference = true;
  var oldPos = state.pos;
  var max = state.posMax;

  if (state.src.charCodeAt(state.pos) !== 0x5b /* [ */) {
    return false;
  }

  var labelStart = state.pos + 1;
  var labelEnd = state.md.helpers.parseLinkLabel(state, state.pos, true);

  if (labelEnd < 0) {
    return false;
  }

  pos = labelEnd + 1;
  if (pos < max && state.src.charCodeAt(pos) === 0x28 /* ( */) {
    parseReference = false;

    pos++;
    for (; pos < max; pos++) {
      code = state.src.charCodeAt(pos);
      if (!isSpace(code) && code !== 0x0a) {
        break;
      }
    }
    if (pos >= max) {
      return false;
    }

    start = pos;
    res = state.md.helpers.parseLinkDestination(state.src, pos, state.posMax);
    if (res.ok) {
      href = state.md.normalizeLink(res.str);
      footnoteContent = res.str;
      if (state.md.validateLink(href)) {
        pos = res.pos;
      } else {
        href = "";
      }
    }

    start = pos;
    for (; pos < max; pos++) {
      code = state.src.charCodeAt(pos);
      if (!isSpace(code) && code !== 0x0a) {
        break;
      }
    }

    res = state.md.helpers.parseLinkTitle(state.src, pos, state.posMax);
    if (pos < max && start !== pos && res.ok) {
      title = res.str;
      pos = res.pos;

      for (; pos < max; pos++) {
        code = state.src.charCodeAt(pos);
        if (!isSpace(code) && code !== 0x0a) {
          break;
        }
      }
    } else {
      title = "";
    }

    if (pos >= max || state.src.charCodeAt(pos) !== 0x29 /* ) */) {
      parseReference = true;
    }
    pos++;
  }

  if (parseReference) {
    if (typeof state.env.references === "undefined") {
      return false;
    }

    if (pos < max && state.src.charCodeAt(pos) === 0x5b /* [ */) {
      start = pos + 1;
      pos = state.md.helpers.parseLinkLabel(state, pos);
      if (pos >= 0) {
        label = state.src.slice(start, pos++);
      } else {
        pos = labelEnd + 1;
      }
    } else {
      pos = labelEnd + 1;
    }

    if (!label) {
      label = state.src.slice(labelStart, labelEnd);
    }

    ref = state.env.references[normalizeReference(label)];
    if (!ref) {
      state.pos = oldPos;
      return false;
    }
    href = ref.href;
    title = ref.title;
  }

  if (!silent) {
    if (title) {
      state.pos = labelStart;
      state.posMax = labelEnd;

      var tokens;

      if (!state.env.footnotes) {
        state.env.footnotes = {};
      }
      if (!state.env.footnotes.list) {
        state.env.footnotes.list = [];
      }

      var footnoteId = state.env.footnotes.list.length;

      state.md.inline.parse(title + ": *" + footnoteContent + "*", state.md, state.env, (tokens = []));

      token = state.push("footnote_word", "", 0);
      token.content = state.src.slice(labelStart, labelEnd);

      token = state.push("footnote_ref", "", 0);
      token.meta = { id: footnoteId };

      state.env.footnotes.list[footnoteId] = { tokens: tokens };
    } else {
      state.pos = labelStart;
      state.posMax = labelEnd;

      token = state.push("link_open", "a", 1);
      attrs = [["href", href]];
      token.attrs = attrs;
      if (title) {
        attrs.push(["title", title]);
      }

      state.md.inline.tokenize(state);

      token = state.push("link_close", "a", -1);
    }
  }

  state.pos = pos;
  state.posMax = max;

  return true;
}

function footnoteTail(state) {
  var i,
    l,
    lastParagraph,
    list,
    token,
    tokens,
    current,
    currentLabel,
    insideRef = false,
    refTokens = {};

  if (!state.env.footnotes) {
    return;
  }

  state.tokens = state.tokens.filter(function (tok) {
    if (tok.type === "footnote_reference_open") {
      insideRef = true;
      current = [];
      currentLabel = tok.meta.label;
      return false;
    }
    if (tok.type === "footnote_reference_close") {
      insideRef = false;
      refTokens[":" + currentLabel] = current;
      return false;
    }
    if (insideRef) {
      current.push(tok);
    }
    return !insideRef;
  });

  if (!state.env.footnotes.list) {
    return;
  }
  list = state.env.footnotes.list;

  token = new state.Token("footnote_block_open", "", 1);
  state.tokens.push(token);

  for (i = 0, l = list.length; i < l; i++) {
    token = new state.Token("footnote_open", "", 1);
    token.meta = { id: i, label: list[i].label };
    state.tokens.push(token);

    if (list[i].tokens) {
      tokens = [];

      token = new state.Token("paragraph_open", "p", 1);
      token.block = true;
      tokens.push(token);

      token = new state.Token("inline", "", 0);
      token.children = list[i].tokens;
      token.content = "";
      tokens.push(token);

      token = new state.Token("paragraph_close", "p", -1);
      token.block = true;
      tokens.push(token);
    } else if (list[i].label) {
      tokens = refTokens[":" + list[i].label];
    }

    state.tokens = state.tokens.concat(tokens);
    if (state.tokens[state.tokens.length - 1].type === "paragraph_close") {
      lastParagraph = state.tokens.pop();
    } else {
      lastParagraph = null;
    }

    if (lastParagraph) {
      state.tokens.push(lastParagraph);
    }

    token = new state.Token("footnote_close", "", -1);
    state.tokens.push(token);
  }

  token = new state.Token("footnote_block_close", "", -1);
  state.tokens.push(token);
}

function markdownItLinkfoot(md) {
  md.renderer.rules.footnote_ref = renderFootnoteRef;
  md.renderer.rules.footnote_word = renderFootnoteWord;
  md.renderer.rules.footnote_block_open = renderFootnoteBlockOpen;
  md.renderer.rules.footnote_block_close = renderFootnoteBlockClose;
  md.renderer.rules.footnote_open = renderFootnoteOpen;
  md.renderer.rules.footnote_close = renderFootnoteClose;

  md.renderer.rules.footnote_caption = renderFootnoteCaption;
  md.renderer.rules.footnote_anchor_name = renderFootnoteAnchorName;

  md.inline.ruler.at("link", linkFoot);
  md.core.ruler.after("inline", "footnote_tail", footnoteTail);
}

window.AutoArticle = window.AutoArticle || {};
window.AutoArticle.plugins = window.AutoArticle.plugins || {};
window.AutoArticle.plugins.markdownItLinkfoot = markdownItLinkfoot;
