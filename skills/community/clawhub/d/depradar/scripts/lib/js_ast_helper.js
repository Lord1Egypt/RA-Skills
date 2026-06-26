#!/usr/bin/env node
/**
 * js_ast_helper.js — Real AST-based JS/TS symbol detection for /depradar.
 *
 * Called by usage_scanner.py when Node.js is available.
 * Input (stdin): JSON { file: string, symbols: string[], package: string }
 * Output (stdout): JSON { [symbol]: [{ file_path, line_number, usage_text, detection_method }] }
 *
 * Uses Node.js built-in 'acorn' parser (available since Node 12 via require('acorn')).
 * Falls back to require-based detection if acorn is not available.
 */

"use strict";

const fs   = require("fs");
const path = require("path");

function main() {
  let input;
  try {
    const raw = fs.readFileSync("/dev/stdin", "utf8");
    input = JSON.parse(raw);
  } catch (e) {
    process.stdout.write(JSON.stringify({}));
    return;
  }

  const { file: filePath, symbols = [], package: pkgName = "" } = input;

  if (!filePath || !symbols.length) {
    process.stdout.write(JSON.stringify({}));
    return;
  }

  let source;
  try {
    source = fs.readFileSync(filePath, "utf8");
  } catch (e) {
    process.stdout.write(JSON.stringify({}));
    return;
  }

  const lines = source.split("\n");
  const result = {};

  // Try acorn for real AST
  let ast = null;
  try {
    const acorn = require("acorn");
    ast = acorn.parse(source, {
      ecmaVersion: "latest",
      sourceType: "module",
      locations: true,
    });
  } catch (e) {
    // Fallback: regex-based (same as Python fallback)
  }

  if (ast) {
    // Walk AST to find symbol references
    const packageAliases = extractPackageAliases(ast, pkgName);
    const destructured   = extractDestructuredSymbols(ast, pkgName);

    for (const sym of symbols) {
      const base = extractBaseSymbol(sym);
      if (!base) continue;

      walkNode(ast, (node) => {
        if (!node || !node.loc) return;
        const lineno = node.loc.start.line;
        const lineText = lines[lineno - 1] || "";

        // High confidence: alias.base access
        if (node.type === "MemberExpression" &&
            node.property.type === "Identifier" &&
            node.property.name === base) {
          const objName = node.object.type === "Identifier" ? node.object.name : null;
          if (objName && packageAliases.has(objName)) {
            addResult(result, sym, filePath, lineno, lineText, "high");
          }
        }

        // Destructured/re-exported/type-only symbol reference
        if (node.type === "Identifier" && node.name === base && destructured.has(node.name)) {
          // Choose detection method based on how the symbol was imported
          let method = "ast";  // default: confirmed destructuring (medium confidence)
          if (_typeOnlySymbols.has(node.name)) {
            method = "type-import";  // type-only: low confidence (no runtime impact)
          } else if (_reExportedSymbols.has(node.name)) {
            method = "re-export";    // barrel re-export: medium confidence
          }
          addResult(result, sym, filePath, lineno, lineText, method);
        }
      });
    }
  } else {
    // Regex fallback
    for (const sym of symbols) {
      const base = extractBaseSymbol(sym);
      if (!base) continue;
      const re = new RegExp(`\\b${escapeRegex(base)}\\b`);
      lines.forEach((line, i) => {
        if (re.test(line)) {
          addResult(result, sym, filePath, i + 1, line.trim(), "grep");
        }
      });
    }
  }

  process.stdout.write(JSON.stringify(result));
}

function addResult(result, sym, filePath, lineno, lineText, method) {
  if (!result[sym]) result[sym] = [];
  // Avoid duplicate line entries
  if (!result[sym].some(r => r.line_number === lineno)) {
    result[sym].push({
      file_path: filePath,
      line_number: lineno,
      usage_text: lineText.trim().slice(0, 200),
      detection_method: method,
    });
  }
}

function extractPackageAliases(ast, pkgName) {
  const aliases = new Set();
  if (!pkgName) return aliases;

  walkNode(ast, (node) => {
    if (!node) return;
    // import stripe from 'stripe'
    if (node.type === "ImportDeclaration" &&
        node.source && node.source.value === pkgName) {
      for (const spec of (node.specifiers || [])) {
        if (spec.type === "ImportDefaultSpecifier" ||
            spec.type === "ImportNamespaceSpecifier") {
          aliases.add(spec.local.name);
        }
      }
    }
    // const stripe = require('stripe')
    if (node.type === "VariableDeclaration") {
      for (const decl of node.declarations) {
        if (decl.init &&
            decl.init.type === "CallExpression" &&
            decl.init.callee.name === "require" &&
            decl.init.arguments[0] &&
            decl.init.arguments[0].value === pkgName &&
            decl.id.type === "Identifier") {
          aliases.add(decl.id.name);
        }
        // const stripe = await import('stripe')
        if (decl.init &&
            decl.init.type === "AwaitExpression" &&
            decl.init.argument &&
            decl.init.argument.type === "ImportExpression" &&
            decl.init.argument.source &&
            decl.init.argument.source.value === pkgName &&
            decl.id && decl.id.type === "Identifier") {
          aliases.add(decl.id.name);
        }
      }
    }
  });

  aliases.add(pkgName); // always include package name itself
  return aliases;
}

// Tracks re-exported and type-only-imported symbols separately for confidence mapping
const _reExportedSymbols = new Set();
const _typeOnlySymbols = new Set();

function extractDestructuredSymbols(ast, pkgName) {
  const syms = new Set();
  if (!pkgName) return syms;

  walkNode(ast, (node) => {
    if (!node) return;
    // import { constructEvent } from 'stripe'
    // import type { TextContent } from '@google/genai'  (type-only — low confidence)
    if (node.type === "ImportDeclaration" &&
        node.source && node.source.value === pkgName) {
      const isTypeOnly = node.importKind === "type";
      for (const spec of (node.specifiers || [])) {
        if (spec.type === "ImportSpecifier") {
          syms.add(spec.local.name);
          if (isTypeOnly) _typeOnlySymbols.add(spec.local.name);
        }
      }
    }
    // export { constructEvent } from 'stripe'  (barrel re-export — med confidence)
    if (node.type === "ExportNamedDeclaration" &&
        node.source && node.source.value === pkgName) {
      for (const spec of (node.specifiers || [])) {
        if (spec.local && spec.local.type === "Identifier") {
          syms.add(spec.local.name);
          _reExportedSymbols.add(spec.local.name);
        }
      }
    }
    // const { constructEvent } = require('stripe')
    if (node.type === "VariableDeclaration") {
      for (const decl of node.declarations) {
        if (decl.init &&
            decl.init.type === "CallExpression" &&
            decl.init.callee.name === "require" &&
            decl.init.arguments[0] &&
            decl.init.arguments[0].value === pkgName &&
            decl.id.type === "ObjectPattern") {
          for (const prop of decl.id.properties) {
            if (prop.value && prop.value.type === "Identifier") {
              syms.add(prop.value.name);
            }
          }
        }
      }
    }
  });

  return syms;
}

function walkNode(node, visitor) {
  if (!node || typeof node !== "object") return;
  visitor(node);
  for (const key of Object.keys(node)) {
    const child = node[key];
    if (Array.isArray(child)) {
      for (const item of child) walkNode(item, visitor);
    } else if (child && typeof child === "object" && child.type) {
      walkNode(child, visitor);
    }
  }
}

function extractBaseSymbol(sym) {
  return sym.replace(/\([^)]*\)$/, "").split(/[.:]/).pop() || sym;
}

function escapeRegex(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

main();
