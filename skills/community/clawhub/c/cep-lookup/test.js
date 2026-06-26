/**
 * test.js — Local test runner for the CEP Lookup skill
 *
 * Usage:
 *   node test.js          → runs with real ViaCEP API calls
 *   node test.js --mock   → runs with mocked responses (no internet needed)
 */

const MOCK_MODE = process.argv.includes('--mock');

// --- Mock axios in mock mode ---
if (MOCK_MODE) {
    const Module = require('module');
    const originalLoad = Module._load;

    Module._load = function (request, ...args) {
        if (request === 'axios') {
            return {
                get: async (url) => {
                    if (url.includes('01001000')) {
                        return {
                            data: {
                                logradouro: 'Praça da Sé',
                                bairro: 'Sé',
                                localidade: 'São Paulo',
                                uf: 'SP',
                                complemento: 'lado ímpar',
                            },
                        };
                    }
                    if (url.includes('00000000')) {
                        return { data: { erro: true } };
                    }
                    throw new Error('Network error');
                },
            };
        }
        return originalLoad(request, ...args);
    };
}

const skill = require('./index');

// Helper: simulate the OpenClaw context object
function makeContext(text) {
    return { message: { text } };
}

// --- Test cases ---
const tests = [
    {
        description: 'Valid CEP with dash',
        input: 'cep 01001-000',
        expect: (result) => result.includes('São Paulo'),
    },
    {
        description: 'Valid CEP without dash',
        input: 'cep 01001000',
        expect: (result) => result.includes('São Paulo'),
    },
    {
        description: 'English-style trigger',
        input: 'What are the details for CEP 01001-000',
        expect: (result) => result.includes('São Paulo'),
    },
    {
        description: 'Uppercase CEP keyword',
        input: 'CEP 01001-000',
        expect: (result) => result.includes('São Paulo'),
    },
    {
        description: 'CEP not found',
        input: 'cep 00000-000',
        expect: (result) => result.includes('not found'),
    },
    {
        description: 'Invalid format (too few digits)',
        input: 'cep 1234',
        expect: (result) => result.includes('Invalid CEP format'),
    },
    {
        description: 'No CEP in message',
        input: 'hello there',
        expect: (result) => result.includes('Invalid CEP format'),
    },
];

// --- Runner ---
async function run() {
    const mode = MOCK_MODE ? 'MOCK' : 'LIVE';
    console.log(`\nRunning CEP Skill tests... [${mode} mode]\n`);

    let passed = 0;
    let failed = 0;

    for (const test of tests) {
        process.stdout.write(`  ${test.description} ... `);
        try {
            const result = await skill(makeContext(test.input));
            const ok = test.expect(result);
            if (ok) {
                console.log('✅ PASS');
                passed++;
            } else {
                console.log('❌ FAIL');
                failed++;
            }
            // Always show the input and result
            console.log(`     Input:  "${test.input}"`);
            console.log(`     Result:`);
            result.split('\n').forEach((line) => console.log(`       ${line}`));
        } catch (err) {
            console.log('💥 ERROR');
            console.log(`     ${err.message}`);
            failed++;
        }
    }

    console.log(`\nResults: ${passed} passed, ${failed} failed out of ${tests.length} tests.\n`);
    process.exit(failed > 0 ? 1 : 0);
}

run();