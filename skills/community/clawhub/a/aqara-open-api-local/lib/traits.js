const fs = require('fs');

const { cliError } = require('./errors');
const { getRuntimeConfig } = require('./config');

function parseBooleanCell(value) {
  return String(value || '').includes('✔');
}

function parseTraitCatalog() {
  const { traitCodesPath } = getRuntimeConfig({ allowMissing: true });
  if (!fs.existsSync(traitCodesPath)) {
    throw cliError('CONFIG_ERROR', 'trait-codes.md was not found', {
      path: traitCodesPath,
    });
  }

  const rawText = fs.readFileSync(traitCodesPath, 'utf8');
  const tableLines = rawText
    .split(/\r?\n/u)
    .filter((line) => line.trim().startsWith('|'));

  if (tableLines.length < 3) {
    throw cliError('CONFIG_ERROR', 'trait-codes.md does not contain a readable markdown table', {
      path: traitCodesPath,
    });
  }

  const dataLines = tableLines.slice(2);
  return dataLines.map((line) => {
    const cells = line
      .split('|')
      .slice(1, -1)
      .map((cell) => cell.trim());

    return {
      traitCode: cells[0] || '',
      traitNameChinese: cells[1] || '',
      traitNameEnglish: cells[2] || '',
      valueType: cells[3] || '',
      unit: cells[4] || '',
      readable: parseBooleanCell(cells[5]),
      writable: parseBooleanCell(cells[6]),
      reportable: parseBooleanCell(cells[7]),
    };
  }).filter((traitItem) => traitItem.traitCode);
}

function filterTraitCatalog(traitCatalog, filters = {}) {
  const {
    query,
    writable,
    readable,
    reportable,
    valueType,
  } = filters;

  return traitCatalog.filter((traitItem) => {
    if (writable !== undefined && traitItem.writable !== writable) {
      return false;
    }
    if (readable !== undefined && traitItem.readable !== readable) {
      return false;
    }
    if (reportable !== undefined && traitItem.reportable !== reportable) {
      return false;
    }
    if (valueType && String(traitItem.valueType).toLowerCase() !== String(valueType).toLowerCase()) {
      return false;
    }
    if (query) {
      const lowerCaseQuery = String(query).toLowerCase();
      const haystack = [
        traitItem.traitCode,
        traitItem.traitNameChinese,
        traitItem.traitNameEnglish,
      ].join(' ').toLowerCase();
      return haystack.includes(lowerCaseQuery);
    }
    return true;
  });
}

function enrichTraitItem(traitCatalogMap, traitItem) {
  const catalogTrait = traitCatalogMap.get(traitItem.traitCode);
  return {
    ...traitItem,
    traitNameChinese: catalogTrait?.traitNameChinese || '',
    traitNameEnglish: catalogTrait?.traitNameEnglish || traitItem.traitName || '',
    catalogValueType: catalogTrait?.valueType || '',
    unit: catalogTrait?.unit || '',
    readable: catalogTrait?.readable,
    writable: catalogTrait?.writable,
    reportable: catalogTrait?.reportable,
  };
}

module.exports = {
  enrichTraitItem,
  filterTraitCatalog,
  parseTraitCatalog,
};
