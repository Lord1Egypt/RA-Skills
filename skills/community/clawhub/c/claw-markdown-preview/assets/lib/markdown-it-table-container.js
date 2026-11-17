function makeTableContainerRule(md) {
  return function addTableContainer(state) {
    var arr = [];
    for (var i = 0; i < state.tokens.length; i++) {
      var curToken = state.tokens[i];
      if (curToken.type === "table_open") {
        var tableContainerStart = new state.Token("html_inline", "", 0);
        tableContainerStart.content = `<section class="table-container">`;
        arr.push(tableContainerStart);
        arr.push(curToken);
      } else if (curToken.type === "table_close") {
        var tableContainerClose = new state.Token("html_inline", "", 0);
        tableContainerClose.content = `</section>`;
        arr.push(curToken);
        arr.push(tableContainerClose);
      } else {
        arr.push(curToken);
      }
    }
    state.tokens = arr;
  };
}

function markdownItTableContainer(md) {
  md.core.ruler.push("table-container", makeTableContainerRule(md));
}

window.AutoArticle = window.AutoArticle || {};
window.AutoArticle.plugins = window.AutoArticle.plugins || {};
window.AutoArticle.plugins.markdownItTableContainer = markdownItTableContainer;