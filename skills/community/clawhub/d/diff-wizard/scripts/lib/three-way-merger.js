/**
 * three-way-merger.js — 3-way merge engine for diff-wizard
 *
 * Implements standard diff3 algorithm to merge base + ours + theirs.
 * Detects conflicts, auto-resolves non-conflicting changes,
 * and provides AI merge suggestions per conflict.
 */

'use strict';

const textDiffer = require('./text-differ');

/**
 * Perform a 3-way merge.
 * @param {string} baseContent - Base (common ancestor) content
 * @param {string} oursContent - Our changes
 * @param {string} theirsContent - Their changes
 * @param {object} [opts]
 * @param {boolean} [opts.autoResolve=false]
 * @param {string} [opts.strategy='manual'] - 'ours', 'theirs', or 'manual'
 * @param {boolean} [opts.generateAiSuggestions=true]
 * @returns {object} Merge result
 */
function threeWayMerge(baseContent, oursContent, theirsContent, opts = {}) {
  const autoResolve = opts.autoResolve || false;
  const strategy = opts.strategy || 'manual';

  // Quick check: if all three are identical
  if (baseContent === oursContent && baseContent === theirsContent) {
    return {
      ok: true,
      mergedContent: baseContent,
      conflicts: [],
      conflictCount: 0,
      autoResolvedCount: 0,
      hasConflicts: false,
      error: null,
    };
  }

  // If base equals ours, accept theirs
  if (baseContent === oursContent) {
    return {
      ok: true,
      mergedContent: theirsContent,
      conflicts: [],
      conflictCount: 0,
      autoResolvedCount: 1,
      hasConflicts: false,
      error: null,
    };
  }

  // If base equals theirs, accept ours
  if (baseContent === theirsContent) {
    return {
      ok: true,
      mergedContent: oursContent,
      conflicts: [],
      conflictCount: 0,
      autoResolvedCount: 1,
      hasConflicts: false,
      error: null,
    };
  }

  // If ours equals theirs, accept either
  if (oursContent === theirsContent) {
    return {
      ok: true,
      mergedContent: oursContent,
      conflicts: [],
      conflictCount: 0,
      autoResolvedCount: 1,
      hasConflicts: false,
      error: null,
    };
  }

  // Compute diffs
  const diffOurs = textDiffer.unifiedDiff(baseContent, oursContent, {
    labelA: 'base', labelB: 'ours', contextLines: 0,
  });
  const diffTheirs = textDiffer.unifiedDiff(baseContent, theirsContent, {
    labelA: 'base', labelB: 'theirs', contextLines: 0,
  });

  // Line-based merge
  const baseLines = baseContent.split('\n');
  const oursLines = oursContent.split('\n');
  const theirsLines = theirsContent.split('\n');

  // Build change maps for both sides
  const oursChanges = buildChangeMap(diffOurs);
  const theirsChanges = buildChangeMap(diffTheirs);

  const merged = [];
  const conflicts = [];
  let conflictIdx = 0;
  let autoResolvedCount = 0;

  // Walk through base lines and apply changes
  let i = 0;
  while (i < baseLines.length) {
    const ourChange = oursChanges.find(c => c.baseStart <= i && i < c.baseEnd);
    const theirChange = theirsChanges.find(c => c.baseStart <= i && i < c.baseEnd);

    if (ourChange && theirChange) {
      // Both changed the same region — potential conflict
      if (ourChange.newText === theirChange.newText) {
        // Same change, accept either
        const lines = ourChange.newText.split('\n');
        merged.push(...lines);
        i = ourChange.baseEnd;
        autoResolvedCount++;
      } else {
        // Real conflict
        if (conflicts.length < 100) {
          conflictIdx++;
          const location = `Lines ${i + 1}-${Math.max(ourChange.baseEnd, theirChange.baseEnd)}`;

          // Generate conflict marker block
          const markerLines = [
            `<<<<<<< ours`,
            ...ourChange.newText.split('\n'),
            `=======`,
            ...theirChange.newText.split('\n'),
            `>>>>>>> theirs`,
          ];

          conflicts.push({
            location,
            base: ourChange.baseText,
            ours: ourChange.newText,
            theirs: theirChange.newText,
            ai_suggestion: null,
          });

          if (strategy === 'ours' && autoResolve) {
            merged.push(...ourChange.newText.split('\n'));
            autoResolvedCount++;
          } else if (strategy === 'theirs' && autoResolve) {
            merged.push(...theirChange.newText.split('\n'));
            autoResolvedCount++;
          } else {
            merged.push(...markerLines);
          }
        }

        i = Math.max(ourChange.baseEnd, theirChange.baseEnd);
      }
    } else if (ourChange) {
      // Only ours changed this region
      const lines = ourChange.newText.split('\n');
      merged.push(...lines);
      i = ourChange.baseEnd;
    } else if (theirChange) {
      // Only theirs changed this region
      const lines = theirChange.newText.split('\n');
      merged.push(...lines);
      i = theirChange.baseEnd;
    } else {
      // No changes — keep base line
      merged.push(baseLines[i]);
      i++;
    }
  }

  const conflictOverflow = conflicts.length >= 100;

  if (opts.generateAiSuggestions !== false && conflicts.length > 0) {
    for (const conflict of conflicts) {
      conflict.ai_suggestion = generateAiSuggestion(conflict);
    }
  }

  const result = {
    ok: true,
    mergedContent: merged.join('\n'),
    conflicts,
    conflictCount: conflicts.length,
    autoResolvedCount,
    hasConflicts: conflicts.length > 0,
    conflictOverflow,
    error: conflictOverflow
      ? 'E008: Too many conflicts (>= 100). Manual resolution recommended.'
      : null,
  };

  return result;
}

/**
 * Build a list of changes from a diff result.
 * Each change has: baseStart, baseEnd, baseText, newText
 */
function buildChangeMap(diffResult) {
  const changes = [];

  if (!diffResult.hunks) return changes;

  for (const hunk of diffResult.hunks) {
    let currentChange = null;
    let baseLine = hunk.startA;

    for (const line of hunk.lines) {
      if (line.type === 'equal') {
        if (currentChange) {
          changes.push(currentChange);
          currentChange = null;
        }
        baseLine++;
      } else if (line.type === 'delete') {
        if (!currentChange) {
          currentChange = {
            baseStart: baseLine,
            baseEnd: baseLine + 1,
            baseText: '',
            newText: '',
          };
        }
        currentChange.baseEnd = baseLine + 1;
        currentChange.baseText += line.text + '\n';
        baseLine++;
      } else if (line.type === 'insert') {
        if (!currentChange) {
          currentChange = {
            baseStart: baseLine,
            baseEnd: baseLine,
            baseText: '',
            newText: '',
          };
        }
        currentChange.newText += line.text + '\n';
      }
    }

    if (currentChange) {
      changes.push(currentChange);
    }
  }

  return changes;
}

/**
 * Generate AI merge suggestion for a conflict.
 * @param {object} conflict
 * @returns {string}
 */
function generateAiSuggestion(conflict) {
  const { base, ours, theirs = '' } = conflict;

  if (!base || base.trim() === '') {
    return 'New content added by both sides. Consider accepting theirs if it includes our changes too.';
  }

  if (!ours || ours.trim() === '') {
    return 'Ours deleted this content while theirs kept/modified it. Accept theirs unless deletion was intentional.';
  }

  if (!theirs || theirs.trim() === '') {
    return 'Theirs deleted this content while ours kept/modified it. Accept ours unless deletion was intentional.';
  }

  if (ours.includes(theirs) || theirs.includes(ours)) {
    return 'One side fully contains the other. Accept the longer version to preserve both changes.';
  }

  const baseLines = base.trim().split('\n');
  const oursLines = ours.trim().split('\n');
  const theirsLines = theirs.trim().split('\n');

  if (baseLines.length === oursLines.length && baseLines.length === theirsLines.length) {
    return 'Both sides modified the same lines. Review manually — the correct result may combine aspects of both changes.';
  }

  if (oursLines.length > baseLines.length && theirsLines.length === baseLines.length) {
    return 'Ours added lines while theirs kept the base. Accept ours to include additions.';
  }

  if (theirsLines.length > baseLines.length && oursLines.length === baseLines.length) {
    return 'Theirs added lines while theirs kept the base. Accept theirs to include additions.';
  }

  return 'Both sides made conflicting changes. Manual review recommended.';
}

module.exports = {
  threeWayMerge,
};
