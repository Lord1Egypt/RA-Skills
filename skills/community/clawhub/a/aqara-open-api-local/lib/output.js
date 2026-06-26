function stringifyValue(value) {
  if (value === null || value === undefined) {
    return '';
  }
  if (typeof value === 'string') {
    return value;
  }
  if (typeof value === 'number' || typeof value === 'boolean') {
    return String(value);
  }
  return JSON.stringify(value);
}

function truncateText(value, width) {
  if (value.length <= width) {
    return value;
  }
  if (width <= 1) {
    return value.slice(0, width);
  }
  return `${value.slice(0, width - 1)}…`;
}

function printTable(rows, columns) {
  if (!rows || rows.length === 0) {
    console.log('(empty)');
    return;
  }

  const widths = columns.map((column) => {
    const headerWidth = column.label.length;
    const maxCellWidth = rows.reduce((currentMaxWidth, row) => {
      const text = stringifyValue(row[column.key]);
      return Math.max(currentMaxWidth, text.length);
    }, 0);
    return Math.min(column.maxWidth || 40, Math.max(headerWidth, maxCellWidth));
  });

  const headerLine = columns
    .map((column, index) => truncateText(column.label, widths[index]).padEnd(widths[index]))
    .join('  ');

  const separatorLine = widths.map((width) => '-'.repeat(width)).join('  ');

  console.log(headerLine);
  console.log(separatorLine);

  rows.forEach((row) => {
    const line = columns
      .map((column, index) => {
        const text = truncateText(stringifyValue(row[column.key]), widths[index]);
        return text.padEnd(widths[index]);
      })
      .join('  ');
    console.log(line);
  });
}

function printJson(payload) {
  console.log(JSON.stringify(payload, null, 2));
}

function printKeyValues(payload) {
  Object.entries(payload).forEach(([key, value]) => {
    console.log(`${key}: ${stringifyValue(value)}`);
  });
}

module.exports = {
  printJson,
  printKeyValues,
  printTable,
  stringifyValue,
};
