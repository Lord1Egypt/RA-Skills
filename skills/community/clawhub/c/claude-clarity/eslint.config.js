const globals = require('globals');

module.exports = [
  {
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        ...globals.node,
        ...globals.es2021,
      },
    },
    rules: {
      'no-unused-vars': ['warn', { 'argsIgnorePattern': '^_', 'varsIgnorePattern': '^_', 'caughtErrorsIgnorePattern': '^_' }],
      'no-console': 'off',
      'no-undef': 'error',
      'no-redeclare': 'error',
      'no-duplicate-case': 'error',
      'no-empty': 'warn',
      'no-extra-semi': 'warn',
      'no-unreachable': 'error',
      'eqeqeq': 'warn',
      'no-var': 'warn',
      'prefer-const': 'warn',
      'prefer-template': 'warn',
      'no-throw-literal': 'error',
      'no-return-await': 'warn',
      'require-await': 'warn',
      'no-async-promise-executor': 'error',
      'no-await-in-loop': 'warn',
      'no-promise-executor-return': 'error',
      'no-misleading-character-class': 'error',
      'no-prototype-builtins': 'error',
      'no-self-compare': 'error',
      'no-template-curly-in-string': 'warn',
      'no-unmodified-loop-condition': 'warn',
      'no-unused-private-class-members': 'warn',
      'no-useless-backreference': 'warn',
      'no-useless-catch': 'warn',
      'no-useless-return': 'warn',
      'no-void': 'warn',
      'no-with': 'error',
      'radix': 'warn',
      'yoda': 'warn',
    },
    ignores: ['node_modules/', 'dist/', 'build/'],
  },
  {
    files: ['src/core/code/code-generator.js'],
    rules: {
      'no-undef': 'off',
    },
  },
  {
    files: ['src/core/code/code-planner.js'],
    rules: {
      'no-undef': 'off',
      'no-unreachable': 'off',
    },
  },
];
