function unescapeXml(value) {
  if (!value) {
    return '';
  }
  return String(value)
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'");
}

export function escapeXml(value) {
  if (value === undefined || value === null) {
    return '';
  }
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

export function extractBlocks(xml, localName) {
  const pattern = new RegExp(
    `<(?:\\w+:)?${localName}\\b[\\s\\S]*?<\\/(?:\\w+:)?${localName}>`,
    'g'
  );
  return xml.match(pattern) || [];
}

export function getTagText(xml, localName) {
  const pattern = new RegExp(
    `<(?:\\w+:)?${localName}\\b[^>]*>([\\s\\S]*?)<\\/(?:\\w+:)?${localName}>`,
    'i'
  );
  const m = xml.match(pattern);
  return m ? unescapeXml(m[1].trim()) : '';
}

export function getAttrValue(xml, localName, attrName) {
  const pattern = new RegExp(`<(?:\\w+:)?${localName}\\b[^>]*\\s${attrName}="([^"]+)"`, 'i');
  const m = xml.match(pattern);
  return m ? unescapeXml(m[1]) : '';
}

export function getNestedTagText(xml, parentName, childName) {
  const parentPattern = new RegExp(
    `<(?:\\w+:)?${parentName}\\b[\\s\\S]*?<\\/(?:\\w+:)?${parentName}>`,
    'i'
  );
  const parentMatch = xml.match(parentPattern);
  if (!parentMatch) {
    return '';
  }
  return getTagText(parentMatch[0], childName);
}

export function getResponseError(xml) {
  const status = getResponseStatus(xml);
  if (!status || status.response_class !== 'Error') {
    return null;
  }

  return {
    code: status.code || 'Error',
    message: status.message || 'Unknown EWS error',
  };
}

export function getResponseStatus(xml) {
  const pattern = /<(?:\w+:)?ResponseMessage\b[^>]*ResponseClass="([^"]+)"[^>]*>([\s\S]*?)<\/(?:\w+:)?ResponseMessage>/i;
  const m = String(xml || '').match(pattern);
  if (!m) {
    return null;
  }

  const responseClass = m[1] || '';
  const block = m[2] || '';
  return {
    response_class: responseClass,
    code: getTagText(block, 'ResponseCode') || '',
    message: getTagText(block, 'MessageText') || '',
  };
}
