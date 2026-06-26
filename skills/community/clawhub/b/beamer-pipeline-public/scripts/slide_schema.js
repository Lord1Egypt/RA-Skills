"use strict";

function isPlainObject(value) {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function isNonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function normalizeEquationNumbers(value) {
  const raw = Array.isArray(value) ? value : (value === undefined || value === null ? [] : [value]);
  const seen = new Set();
  const numbers = [];
  for (let item of raw) {
    if (isPlainObject(item)) {
      item = item.number ?? item.label ?? item.id ?? item.text;
    }
    let text = String(item ?? "").trim();
    if (!text) continue;
    text = text.replace(/^Eq(?:uation)?\.?\s*/i, "").trim();
    if (text.startsWith("(") && text.endsWith(")") && text.length >= 2) {
      text = text.slice(1, -1).trim();
    }
    if (!text || seen.has(text)) continue;
    seen.add(text);
    numbers.push(text);
  }
  return numbers;
}

function equationNumbersFromEntry(entry) {
  if (!isPlainObject(entry)) return [];
  for (const key of ["equation_numbers", "equation_number", "numbers", "number", "equation_ids", "equation_refs"]) {
    const numbers = normalizeEquationNumbers(entry[key]);
    if (numbers.length > 0) return numbers;
  }
  return normalizeEquationNumbers(entry.label ?? entry.tag ?? entry.source_label);
}

function isNumberedEquationRef(value) {
  return /^[A-Za-z]?\d+(?:\.\d+)?$/.test(String(value || "").trim());
}

function equationRefLabel(numbers) {
  const cleaned = (Array.isArray(numbers) ? numbers : []).map((number) => String(number || "").trim()).filter(Boolean);
  if (cleaned.length === 0) return "";
  if (cleaned.every((number) => isNumberedEquationRef(number))) {
    return `Eq. (${cleaned.join(", ")})`;
  }
  return cleaned.join("；");
}

function latexFromFormulaLikeEquationNumbers(numbers) {
  const formulaParts = (Array.isArray(numbers) ? numbers : [])
    .map((number) => String(number || "").trim())
    .filter((number) => number && !isNumberedEquationRef(number) && /[=<>_\\^{}]/.test(number))
    .map((number) => number.replace(/sum_/g, "\\sum_"));
  return formulaParts.join("\\quad ");
}

function canonicalEquationBlockEntry(entry) {
  if (isPlainObject(entry)) {
    const equationNumbers = equationNumbersFromEntry(entry);
    const label = entry.label ?? entry.tag ?? entry.source_label ?? equationRefLabel(equationNumbers);
    const latex = entry.latex
      ?? entry.equation
      ?? entry.math
      ?? entry.formula
      ?? entry.tex
      ?? entry.display_latex
      ?? entry.source_latex
      ?? entry.text
      ?? entry.content
      ?? latexFromFormulaLikeEquationNumbers(equationNumbers);
    if (!isNonEmptyString(String(label ?? "")) && !isNonEmptyString(String(latex ?? "")) && equationNumbers.length === 0) {
      return null;
    }
    return {
      ...entry,
      type: "equation",
      label,
      latex,
      equation_numbers: equationNumbers.length > 0 ? equationNumbers : entry.equation_numbers,
      explanation: entry.explanation ?? entry.description ?? entry.caption ?? entry.notes ?? "",
    };
  }
  if (typeof entry === "string" || typeof entry === "number") {
    const latex = String(entry).trim();
    if (!latex) return null;
    return {
      type: "equation",
      label: "",
      latex,
      explanation: "",
    };
  }
  return null;
}

function appendCanonicalEquationBlock(target, seen, entry) {
  const canonical = canonicalEquationBlockEntry(entry);
  if (!canonical) return;
  const key = `${String(canonical.label || "").trim()}\n${String(canonical.latex || "").trim()}`;
  if (seen.has(key)) return;
  seen.add(key);
  target.push(canonical);
}

function equationBlockEntriesFromStructuredValue(value) {
  const entries = [];
  for (const key of ["equation_blocks", "visible_equation_blocks", "equations", "formulae"]) {
    if (Array.isArray(value?.[key])) {
      entries.push(...value[key]);
    }
  }
  return entries;
}

function equationBlocksFromStructuredValue(value) {
  const equations = [];
  const seen = new Set();
  const blocks = Array.isArray(value?.blocks) ? value.blocks : [];
  for (const block of blocks) {
    if (!isPlainObject(block)) continue;
    if (String(block.type || "").toLowerCase() !== "equation") continue;
    appendCanonicalEquationBlock(equations, seen, block);
  }
  for (const entry of equationBlockEntriesFromStructuredValue(value)) {
    appendCanonicalEquationBlock(equations, seen, entry);
  }
  return equations;
}

function normalizeSlideEquationBlockAliases(slide) {
  if (!isPlainObject(slide) || !Array.isArray(slide.visible_equation_blocks) || slide.visible_equation_blocks.length === 0) {
    return slide;
  }
  const normalizedEquationBlocks = equationBlockEntriesFromStructuredValue({
    equation_blocks: Array.isArray(slide.equation_blocks) ? slide.equation_blocks : [],
    visible_equation_blocks: slide.visible_equation_blocks,
  }).map((entry) => canonicalEquationBlockEntry(entry)).filter(Boolean);
  const next = {
    ...slide,
    equation_blocks: normalizedEquationBlocks,
  };
  delete next.visible_equation_blocks;
  return next;
}

function normalizeSlideShapeAliases(slide) {
  if (!isPlainObject(slide)) return slide;
  let next = slide;
  const setAlias = (key, value) => {
    if (!isNonEmptyString(value) || isNonEmptyString(next[key])) return;
    if (next === slide) next = { ...slide };
    next[key] = String(value).trim();
  };
  setAlias("kind", slide.page_kind ?? slide.page_role ?? slide.slide_kind ?? slide.role);
  setAlias("bucket", slide.bucket ?? slide.part ?? slide.ownership);
  if (isNonEmptyString(next.bucket)) {
    const normalizedBucket = String(next.bucket).trim().toLowerCase();
    if (["front_matter", "frontmatter", "opening", "title"].includes(normalizedBucket)) {
      if (next === slide) next = { ...slide };
      next.bucket = "body";
    }
  }
  if (!Array.isArray(next.bullets)) {
    const planned = Array.isArray(slide.planned_visible_bullets)
      ? slide.planned_visible_bullets
      : (Array.isArray(slide.planned_visible_elements) ? slide.planned_visible_elements : null);
    if (planned && planned.length > 0) {
      if (next === slide) next = { ...slide };
      next.bullets = planned;
    }
  }
  return next;
}

function normalizeSlideCollection(slides) {
  if (!Array.isArray(slides)) return [];
  let changedAny = false;
  const normalized = slides.map((slide) => {
    const nextSlide = normalizeSlideShapeAliases(normalizeSlideEquationBlockAliases(slide));
    if (nextSlide !== slide) {
      changedAny = true;
    }
    return nextSlide;
  });
  return changedAny ? normalized : slides;
}

module.exports = {
  equationBlockEntriesFromStructuredValue,
  equationBlocksFromStructuredValue,
  normalizeSlideCollection,
  normalizeSlideEquationBlockAliases,
  normalizeSlideShapeAliases,
};
