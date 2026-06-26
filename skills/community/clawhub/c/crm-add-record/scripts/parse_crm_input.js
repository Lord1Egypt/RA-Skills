#!/usr/bin/env node
/**
 * CRM Input Parser
 * Extracts structured information from natural language CRM input.
 */

function parseCRMInput(userInput) {
    const result = {
        phone: '',
        contact: '',
        region: '',
        basicInfo: ''
    };

    // Remove common punctuation and normalize
    let text = userInput
        .replace(/[，。、]/g, ' ')
        .replace(/,/g, ' ')
        .trim();

    // Extract phone number (11 digits starting with 1)
    const phoneMatch = text.match(/1[3-9]\d{9}/);
    if (phoneMatch) {
        result.phone = phoneMatch[0];
        text = text.replace(result.phone, '').trim();
    }

    // Extract contact name (Chinese characters 1-3 chars, optional title)
    const contactMatch = text.match(/([\u4e00-\u9fa5]{1,3})(?:先生|女士|总|经理|主任)?/);
    if (contactMatch) {
        result.contact = contactMatch[0];
        text = text.replace(result.contact, '').trim();
    }

    // Extract region (city/province 2-4 Chinese chars with optional suffix)
    const regionKeywords = ['省', '市', '区', '县', '地区', '区域'];
    const regionPattern = new RegExp(`([\\u4e00-\\u9fa5]{2,4})(?:${regionKeywords.join('|')})?`);
    const regionMatch = text.match(regionPattern);
    if (regionMatch) {
        result.region = regionMatch[0];
        text = text.replace(result.region, '').trim();
    }

    // Remaining text goes to basicInfo
    result.basicInfo = text.replace(/\s+/g, ' ').trim();

    return result;
}

// Main entry point
const userInput = process.argv[2];
if (!userInput) {
    console.error('Usage: parse_crm_input.js "<user_input>"');
    process.exit(1);
}

const result = parseCRMInput(userInput);
console.log(JSON.stringify(result, null, 2, {
    ensure_ascii: false
}));
