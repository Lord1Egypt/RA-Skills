function isValidDelim(state, pos) {
  var prevChar, nextChar, max = state.posMax, can_open = true, can_close = true;

  prevChar = pos > 0 ? state.src.charCodeAt(pos - 1) : -1;
  nextChar = pos + 1 <= max ? state.src.charCodeAt(pos + 1) : -1;

  if (prevChar === 0x20 || prevChar === 0x09 || (nextChar >= 0x30 && nextChar <= 0x39)) {
    can_close = false;
  }
  if (nextChar === 0x20 || nextChar === 0x09) {
    can_open = false;
  }

  return { can_open: can_open, can_close: can_close };
}

function math_inline(state, silent) {
  var start, match, token, res, pos;

  if (state.src[state.pos] !== "$") {
    return false;
  }

  res = isValidDelim(state, state.pos);
  if (!res.can_open) {
    if (!silent) {
      state.pending += "$";
    }
    state.pos += 1;
    return true;
  }

  start = state.pos + 1;
  match = start;
  while ((match = state.src.indexOf("$", match)) !== -1) {
    pos = match - 1;
    while (state.src[pos] === "\\") {
      pos -= 1;
    }
    if ((match - pos) % 2 == 1) {
      break;
    }
    match += 1;
  }

  if (match === -1) {
    if (!silent) {
      state.pending += "$";
    }
    state.pos = start;
    return true;
  }

  if (match - start === 0) {
    if (!silent) {
      state.pending += "$$";
    }
    state.pos = start + 1;
    return true;
  }

  res = isValidDelim(state, match);
  if (!res.can_close) {
    if (!silent) {
      state.pending += "$";
    }
    state.pos = start;
    return true;
  }

  if (!silent) {
    token = state.push("math_inline", "math", 0);
    token.markup = "$";
    token.content = state.src.slice(start, match);
  }

  state.pos = match + 1;
  return true;
}

function math_block(state, start, end, silent) {
  var firstLine, lastLine, next, lastPos, found = false, token;
  var pos = state.bMarks[start] + state.tShift[start];
  var max = state.eMarks[start];

  if (pos + 2 > max) {
    return false;
  }
  if (state.src.slice(pos, pos + 2) !== "$$") {
    return false;
  }

  pos += 2;
  firstLine = state.src.slice(pos, max);

  if (silent) {
    return true;
  }
  if (firstLine.trim().slice(-2) === "$$") {
    firstLine = firstLine.trim().slice(0, -2);
    found = true;
  }

  for (next = start; !found; ) {
    next++;
    if (next >= end) {
      break;
    }
    pos = state.bMarks[next] + state.tShift[next];
    max = state.eMarks[next];
    if (pos < max && state.tShift[next] < state.blkIndent) {
      break;
    }
    if (state.src.slice(pos, max).trim().slice(-2) === "$$") {
      lastPos = state.src.slice(0, max).lastIndexOf("$$");
      lastLine = state.src.slice(pos, lastPos);
      found = true;
    }
  }

  state.line = next + 1;

  token = state.push("math_block", "math", 0);
  token.block = true;
  token.content =
    (firstLine && firstLine.trim() ? firstLine + "\n" : "") +
    state.getLines(start + 1, next, state.tShift[start], true) +
    (lastLine && lastLine.trim() ? lastLine : "");
  token.map = [start, state.line];
  token.markup = "$$";
  return true;
}

function markdownItMath(md, options) {
  options = options || {};

  var katexInline = function(latex) {
    options.displayMode = false;
    try {
      return "$" + latex + "$";
    } catch (error) {
      return latex;
    }
  };

  var inlineRenderer = function(tokens, idx) {
    return katexInline(tokens[idx].content);
  };

  var katexBlock = function(latex) {
    options.displayMode = true;
    try {
      return "$$" + latex + "$$";
    } catch (error) {
      return latex;
    }
  };

  var blockRenderer = function(tokens, idx) {
    return katexBlock(tokens[idx].content) + "\n";
  };

  md.inline.ruler.after("escape", "math_inline", math_inline);
  md.block.ruler.after("blockquote", "math_block", math_block, {
    alt: ["paragraph", "reference", "blockquote", "list"],
  });
  md.renderer.rules.math_inline = inlineRenderer;
  md.renderer.rules.math_block = blockRenderer;
}

window.AutoArticle = window.AutoArticle || {};
window.AutoArticle.plugins = window.AutoArticle.plugins || {};
window.AutoArticle.plugins.markdownItMath = markdownItMath;