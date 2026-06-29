#!/usr/bin/env node
/**
 * validate-schema.js — Validates a Douyin script output against the schema.
 *
 * Usage:
 *   node validate-schema.js < path/to/output.json
 *   node validate-schema.js --file output.json
 */

const fs = require('fs');
const path = require('path');

const SCHEMA_PATH = path.join(__dirname, '..', 'schemas', 'output.schema.json');

function loadSchema() {
    return JSON.parse(fs.readFileSync(SCHEMA_PATH, 'utf8'));
}

function validate(data) {
    const errors = [];

    // Check required top-level fields
    const required = ['title', 'duration', 'version', 'scenes', 'subtitles', 'bgm', 'publishTime'];
    for (const field of required) {
        if (!(field in data)) {
            errors.push(`Missing required field: "${field}"`);
        }
    }

    // Check duration
    if (data.duration && ![15, 30, 60].includes(data.duration)) {
        errors.push(`"duration" must be 15, 30, or 60, got ${data.duration}`);
    }

    // Check scenes
    if (data.scenes) {
        if (!Array.isArray(data.scenes)) {
            errors.push('"scenes" must be an array');
        } else {
            if (data.scenes.length < 3) {
                errors.push(`"scenes" must have at least 3 items, got ${data.scenes.length}`);
            }
            data.scenes.forEach((scene, i) => {
                ['timeRange', 'visual', 'voiceover', 'cameraAngle', 'shotType'].forEach(f => {
                    if (!(f in scene)) errors.push(`scenes[${i}].${f} is required`);
                });
            });
        }
    }

    // Check subtitles
    if (data.subtitles) {
        if (!data.subtitles.style) errors.push('"subtitles.style" is required');
        if (!Array.isArray(data.subtitles.highlightKeywords)) {
            errors.push('"subtitles.highlightKeywords" must be an array');
        }
    }

    // Check BGM
    if (data.bgm) {
        ['genre', 'pace', 'exampleTracks'].forEach(f => {
            if (!(f in data.bgm)) errors.push(`"bgm.${f}" is required`);
        });
        if (data.bgm.exampleTracks && !Array.isArray(data.bgm.exampleTracks)) {
            errors.push('"bgm.exampleTracks" must be an array');
        }
    }

    // Check publishTime
    if (data.publishTime && !Array.isArray(data.publishTime)) {
        errors.push('"publishTime" must be an array');
    }

    return {
        valid: errors.length === 0,
        errors,
        fieldCount: Object.keys(data).length,
        sceneCount: Array.isArray(data.scenes) ? data.scenes.length : 0
    };
}

// ── CLI ────────────────────────────────────────────────────────────────────
function main() {
    const args = process.argv.slice(2);
    let raw;

    if (args.includes('--file')) {
        const idx = args.indexOf('--file');
        const filePath = args[idx + 1];
        raw = fs.readFileSync(filePath, 'utf8');
    } else if (args.includes('--stdin') || args.length === 0) {
        raw = fs.readFileSync('/dev/stdin', 'utf8');
    } else {
        console.error('Usage: node validate-schema.js [--file <path>]');
        console.error('   or: node validate-schema.js < output.json');
        process.exit(1);
    }

    let data;
    try {
        data = JSON.parse(raw);
    } catch (e) {
        console.error('❌ Invalid JSON:', e.message);
        process.exit(1);
    }

    const result = validate(data);
    if (result.valid) {
        console.log('✅ Output is valid.');
        console.log(`   Fields: ${result.fieldCount}, Scenes: ${result.sceneCount}`);
        process.exit(0);
    } else {
        console.log('❌ Output validation failed:');
        result.errors.forEach(e => console.log(`   • ${e}`));
        process.exit(1);
    }
}

if (require.main === module) main();

module.exports = { validate, loadSchema };
