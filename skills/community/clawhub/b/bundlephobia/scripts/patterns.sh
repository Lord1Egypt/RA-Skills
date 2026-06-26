#!/usr/bin/env bash
# BundlePhobia — Detection Pattern Definitions
# Each pattern: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical — Massive bundle bloat, immediate action needed
#   high     — Significant size impact, should be addressed
#   medium   — Moderate bloat or best practice violation
#   low      — Minor optimization opportunity
#
# IMPORTANT: All regexes must use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [0-9] instead of \d
# - Use [a-zA-Z0-9_] instead of \w
# - Avoid Perl-only features

set -euo pipefail

# ═══════════════════════════════════════════════════════════════════════════
# 1. OVERSIZED DEPENDENCIES (OD-001 through OD-020)
# Known bloated packages with lighter alternatives
# ═══════════════════════════════════════════════════════════════════════════

declare -a BUNDLEPHOBIA_OVERSIZED_PATTERNS=()

BUNDLEPHOBIA_OVERSIZED_PATTERNS+=(
  # moment.js — 290KB+ minified, 72KB+ gzipped
  '"moment"[[:space:]]*:|from[[:space:]]+["\x27]moment["\x27]|require\([[:space:]]*["\x27]moment["\x27]\)|critical|OD-001|moment.js detected (290KB+ minified) — massive bundle impact|Replace with date-fns (tree-shakeable, 12KB) or dayjs (2KB drop-in replacement)'

  # lodash full import — 72KB+ minified
  '"lodash"[[:space:]]*:|from[[:space:]]+["\x27]lodash["\x27]|require\([[:space:]]*["\x27]lodash["\x27]\)|high|OD-002|Full lodash import (72KB+) — not tree-shakeable|Use lodash-es for tree-shaking, or cherry-pick: import debounce from lodash/debounce'

  # faker.js in production — 3.2MB+
  '"faker"[[:space:]]*:|"@faker-js/faker"[[:space:]]*:|high|OD-003|faker.js in dependencies (3.2MB+) — likely test/dev only|Move to devDependencies: npm install --save-dev @faker-js/faker'

  # aws-sdk v2 — 40MB+ full package
  '"aws-sdk"[[:space:]]*:|from[[:space:]]+["\x27]aws-sdk["\x27]|require\([[:space:]]*["\x27]aws-sdk["\x27]\)|critical|OD-004|aws-sdk v2 (40MB+) — includes ALL AWS services|Use modular @aws-sdk/* v3 clients: @aws-sdk/client-s3, @aws-sdk/client-dynamodb, etc.'

  # chart.js full import
  'from[[:space:]]+["\x27]chart\.js["\x27]|require\([[:space:]]*["\x27]chart\.js["\x27]\)|medium|OD-005|chart.js full import — includes all chart types|Use tree-shakeable import: import { Chart } from chart.js/auto or register only needed components'

  # underscore.js — use native ES methods
  '"underscore"[[:space:]]*:|from[[:space:]]+["\x27]underscore["\x27]|require\([[:space:]]*["\x27]underscore["\x27]\)|medium|OD-006|underscore.js detected — native ES methods cover most use cases|Replace with native Array/Object methods (map, filter, reduce, Object.entries, etc.)'

  # jQuery in modern project
  '"jquery"[[:space:]]*:|from[[:space:]]+["\x27]jquery["\x27]|require\([[:space:]]*["\x27]jquery["\x27]\)|medium|OD-007|jQuery detected in project — 90KB+ minified|Remove jQuery; use native DOM APIs or framework-provided utilities'

  # rxjs full import
  'from[[:space:]]+["\x27]rxjs["\x27]|require\([[:space:]]*["\x27]rxjs["\x27][[:space:]]*\)|high|OD-008|Full rxjs import — pulls in entire library|Use specific imports: import { Observable } from rxjs or import { map } from rxjs/operators'

  # crypto-browserify — 420KB+
  '"crypto-browserify"[[:space:]]*:|medium|OD-009|crypto-browserify (420KB+) — polyfill for Node crypto|Use Web Crypto API (window.crypto.subtle) or lighter alternatives like tweetnacl'

  # jsdom in frontend — 20MB+
  '"jsdom"[[:space:]]*:|medium|OD-010|jsdom in dependencies (20MB+) — server-side DOM library|Move to devDependencies if used for testing; never include in frontend bundles'

  # bluebird — native Promises are sufficient
  '"bluebird"[[:space:]]*:|from[[:space:]]+["\x27]bluebird["\x27]|low|OD-011|bluebird Promise library — native Promises are now sufficient|Remove bluebird; use native Promise with async/await'

  # request package — deprecated, 1MB+
  '"request"[[:space:]]*:|from[[:space:]]+["\x27]request["\x27]|high|OD-012|request package detected — deprecated and bloated (1MB+)|Use native fetch(), node-fetch, axios, or undici instead'

  # core-js full polyfill — 200KB+
  '"core-js"[[:space:]]*:[[:space:]]*"[^"]*"[[:space:]]*$|high|OD-013|core-js full polyfill (200KB+) — may include unnecessary polyfills|Use core-js with @babel/preset-env useBuiltIns: usage for targeted polyfilling'

  # material-ui icons full import
  'from[[:space:]]+["\x27]@mui/icons-material["\x27]|from[[:space:]]+["\x27]@material-ui/icons["\x27]|high|OD-014|Material UI icons full import — pulls in ALL icons (5MB+)|Import specific icons: import DeleteIcon from @mui/icons-material/Delete'

  # antd full import
  'from[[:space:]]+["\x27]antd["\x27]|require\([[:space:]]*["\x27]antd["\x27]\)|high|OD-015|Ant Design full import — massive bundle without tree-shaking|Use babel-plugin-import or import specific components: import { Button } from antd/es/button'

  # pdf.js full import — 1.2MB+
  '"pdfjs-dist"[[:space:]]*:|from[[:space:]]+["\x27]pdfjs-dist["\x27]|medium|OD-016|pdfjs-dist full import (1.2MB+) — heavy PDF library|Use dynamic import() for PDF functionality; lazy-load only when needed'

  # three.js — 600KB+
  'from[[:space:]]+["\x27]three["\x27]|require\([[:space:]]*["\x27]three["\x27]\)|medium|OD-017|three.js full import (600KB+) — 3D library|Import specific modules: import { Scene } from three/src/scenes/Scene'

  # firebase full SDK — 200KB+
  'from[[:space:]]+["\x27]firebase["\x27]|require\([[:space:]]*["\x27]firebase["\x27]\)|high|OD-018|Firebase full SDK import — includes all services|Use modular imports: import { getAuth } from firebase/auth'

  # graphql — 80KB+ (often bundled unnecessarily)
  '"graphql"[[:space:]]*:[[:space:]]*"[^"]*"|medium|OD-019|graphql package in production (80KB+) — often only needed at build time|Check if graphql is needed at runtime; move to devDependencies if only for codegen'

  # typescript in production deps — 40MB+
  '"typescript"[[:space:]]*:[[:space:]]*"[^"]*"[[:space:]]*$|high|OD-020|typescript in production dependencies — 40MB+ dev tool|Move to devDependencies: npm install --save-dev typescript'
)

# ═══════════════════════════════════════════════════════════════════════════
# 2. DUPLICATE & REDUNDANT PACKAGES (DD-001 through DD-018)
# Multiple packages serving the same purpose
# ═══════════════════════════════════════════════════════════════════════════

declare -a BUNDLEPHOBIA_DUPLICATE_PATTERNS=()

BUNDLEPHOBIA_DUPLICATE_PATTERNS+=(
  # Both axios and node-fetch
  'PLACEHOLDER_BOTH_AXIOS_FETCH|medium|DD-001|Both axios and node-fetch detected — redundant HTTP clients|Choose one HTTP client; prefer native fetch() in Node 18+'

  # Both moment and dayjs
  'PLACEHOLDER_BOTH_MOMENT_DAYJS|high|DD-002|Both moment.js and dayjs detected — redundant date libraries|Remove moment.js; dayjs is the lighter alternative (2KB vs 290KB)'

  # Both lodash and underscore
  'PLACEHOLDER_BOTH_LODASH_UNDERSCORE|high|DD-003|Both lodash and underscore detected — redundant utility libraries|Remove underscore; use lodash-es or native methods'

  # Both express and koa
  'PLACEHOLDER_BOTH_EXPRESS_KOA|medium|DD-004|Both express and koa detected — redundant web frameworks|Choose one web framework to reduce dependencies'

  # Both jest and mocha
  'PLACEHOLDER_BOTH_JEST_MOCHA|medium|DD-005|Both jest and mocha detected — redundant test runners|Standardize on one test runner to simplify dependencies'

  # Multiple CSS-in-JS libraries
  'PLACEHOLDER_MULTI_CSS_IN_JS|medium|DD-006|Multiple CSS-in-JS libraries detected — redundant styling solutions|Standardize on one CSS-in-JS solution to reduce bundle size'

  # Both uuid and nanoid
  'PLACEHOLDER_BOTH_UUID_NANOID|low|DD-007|Both uuid and nanoid detected — redundant ID generators|Choose one: nanoid (130B) is much smaller than uuid (12KB)'

  # Both winston and bunyan/pino
  'PLACEHOLDER_BOTH_LOGGERS|low|DD-008|Multiple logging libraries detected — redundant loggers|Standardize on one logging library'

  # Both node-fetch and isomorphic-fetch
  'PLACEHOLDER_BOTH_FETCH_POLYFILLS|medium|DD-009|Both node-fetch and isomorphic-fetch detected|Use native fetch() or choose one polyfill'

  # Both dotenv and env-cmd
  'PLACEHOLDER_BOTH_ENV_LIBS|low|DD-010|Both dotenv and env-cmd detected — redundant env loaders|Choose one environment variable solution'

  # Both chalk and colors
  'PLACEHOLDER_BOTH_CHALK_COLORS|low|DD-011|Both chalk and colors detected — redundant terminal color libraries|Choose one; chalk is actively maintained'

  # Both yargs and commander
  'PLACEHOLDER_BOTH_CLI_PARSERS|low|DD-012|Both yargs and commander detected — redundant CLI argument parsers|Choose one CLI argument parser'

  # Both supertest and request for testing
  'PLACEHOLDER_BOTH_HTTP_TEST|low|DD-013|Multiple HTTP testing libraries detected|Standardize on one HTTP testing approach'

  # Both sinon and jest mocks
  'PLACEHOLDER_BOTH_MOCK_LIBS|low|DD-014|Both sinon and jest — jest has built-in mocking|If using jest, remove sinon; jest.fn() and jest.mock() cover most use cases'

  # Both core-js and babel-polyfill
  'PLACEHOLDER_BOTH_POLYFILLS|high|DD-015|Both core-js and babel-polyfill — duplicate polyfills|Remove babel-polyfill (deprecated); use core-js with @babel/preset-env useBuiltIns: usage'

  # Both webpack and rollup
  'PLACEHOLDER_BOTH_BUNDLERS|medium|DD-016|Both webpack and rollup detected — unusual dual-bundler setup|Consolidate to one bundler unless intentionally using both for different targets'

  # Both prop-types and typescript
  'PLACEHOLDER_BOTH_TYPECHECK|low|DD-017|Both prop-types and typescript detected — redundant type checking|TypeScript interfaces replace prop-types; remove prop-types to reduce bundle'

  # Both body-parser and express 4.16+
  '"body-parser"[[:space:]]*:|low|DD-018|body-parser as separate package — built into Express 4.16+|Remove body-parser; use express.json() and express.urlencoded() instead'
)

# ═══════════════════════════════════════════════════════════════════════════
# 3. TREE-SHAKING FAILURES (TS-001 through TS-020)
# Code patterns that prevent dead-code elimination
# ═══════════════════════════════════════════════════════════════════════════

declare -a BUNDLEPHOBIA_TREESHAKE_PATTERNS=()

BUNDLEPHOBIA_TREESHAKE_PATTERNS+=(
  # import * as namespace — prevents tree-shaking
  'import[[:space:]]+\*[[:space:]]+as[[:space:]]+[a-zA-Z_]+[[:space:]]+from[[:space:]]+["\x27]lodash|high|TS-001|import * from lodash — prevents tree-shaking entirely|Use named imports: import { debounce } from lodash-es'

  # require() instead of import
  'require\([[:space:]]*["\x27][a-zA-Z@][a-zA-Z0-9@/_-]+["\x27][[:space:]]*\)|medium|TS-002|CommonJS require() — prevents tree-shaking|Use ES import syntax: import x from pkg for tree-shaking support'

  # dynamic require
  'require\([[:space:]]*[a-zA-Z_]|high|TS-003|Dynamic require() with variable — prevents static analysis|Use dynamic import() for code splitting or restructure to static imports'

  # barrel file export *
  'export[[:space:]]+\*[[:space:]]+from[[:space:]]+["\x27]|medium|TS-004|Barrel file re-export (export * from) — may prevent tree-shaking|Use explicit named exports instead of wildcard re-exports'

  # module.exports mixed with ESM
  'module\.exports[[:space:]]*=|medium|TS-005|CommonJS module.exports — not tree-shakeable|Convert to ES module export syntax: export default or export { name }'

  # Side-effect import of large lib
  'import[[:space:]]+["\x27]lodash["\x27]|import[[:space:]]+["\x27]rxjs["\x27]|high|TS-006|Side-effect import of large library — loads entire package|Use named imports: import { specific } from pkg'

  # Namespace import of tree-shakeable lib
  'import[[:space:]]+\*[[:space:]]+as[[:space:]]+[a-zA-Z_]+[[:space:]]+from[[:space:]]+["\x27]rxjs|high|TS-007|Namespace import of rxjs — defeats tree-shaking|Use named imports: import { Observable, map } from rxjs'

  # import * as from date-fns
  'import[[:space:]]+\*[[:space:]]+as[[:space:]]+[a-zA-Z_]+[[:space:]]+from[[:space:]]+["\x27]date-fns|high|TS-008|Namespace import of date-fns — defeats tree-shaking|Use named imports: import { format, parseISO } from date-fns'

  # Require entire AWS SDK
  'require\([[:space:]]*["\x27]aws-sdk["\x27][[:space:]]*\)|critical|TS-009|require() of aws-sdk — pulls in entire 40MB+ SDK|Use modular @aws-sdk/* v3 with ES imports'

  # import * as from @mui/material
  'import[[:space:]]+\*[[:space:]]+as[[:space:]]+[a-zA-Z_]+[[:space:]]+from[[:space:]]+["\x27]@mui|high|TS-010|Namespace import of MUI — imports all components|Use named imports: import { Button, TextField } from @mui/material'

  # import from barrel index
  'from[[:space:]]+["\x27]\.\./\.\./\.\./index["\x27]|from[[:space:]]+["\x27]\.\./\.\./index["\x27]|medium|TS-011|Deep import from barrel index file — may cause large re-exports|Import directly from the source module, not the index barrel'

  # Re-exporting everything in index
  'export[[:space:]]+\{[[:space:]]*\}[[:space:]]+from|export[[:space:]]+\*[[:space:]]+from[[:space:]]+["\x27]\./|medium|TS-012|Index file re-exporting all modules — barrel file anti-pattern|Export only what is needed from index or import directly from modules'

  # import * as from react-icons
  'import[[:space:]]+\*[[:space:]]+as[[:space:]]+[a-zA-Z_]+[[:space:]]+from[[:space:]]+["\x27]react-icons|high|TS-013|Namespace import of react-icons — imports ALL icon packs|Import specific icons: import { FaHome } from react-icons/fa'

  # Default import of lodash-es (fine, but check usage)
  'import[[:space:]]+_[[:space:]]+from[[:space:]]+["\x27]lodash-es["\x27]|medium|TS-014|Default import of lodash-es — may import full bundle|Use named imports: import { debounce, throttle } from lodash-es'

  # Namespace import from utils barrel
  'import[[:space:]]+\*[[:space:]]+as[[:space:]]+[a-zA-Z_]+[[:space:]]+from[[:space:]]+["\x27]\./utils["\x27]|medium|TS-015|Namespace import from utils barrel — prevents tree-shaking|Use named imports from specific util files'

  # CommonJS interop — __esModule
  'exports\.__esModule[[:space:]]*=|low|TS-016|CommonJS __esModule interop detected — mixed module system|Convert module to pure ES modules for better tree-shaking'

  # Object.defineProperty exports
  'Object\.defineProperty\([[:space:]]*exports|low|TS-017|Object.defineProperty on exports — CJS output pattern|Ensure bundler outputs ESM format for tree-shaking'

  # eval() prevents optimization
  'eval[[:space:]]*\(|medium|TS-018|eval() call detected — prevents bundler optimizations|Remove eval(); use Function constructor or other alternatives if dynamic code is needed'

  # with statement prevents optimization
  'with[[:space:]]*\(|medium|TS-019|with statement detected — prevents bundler optimizations|Remove with statement; use destructuring or variable assignments instead'

  # Import entire icon library
  'from[[:space:]]+["\x27]@fortawesome/free-solid-svg-icons["\x27]|high|TS-020|Full FontAwesome icon import — pulls all icons|Import specific icons: import { faHome } from @fortawesome/free-solid-svg-icons/faHome'
)

# ═══════════════════════════════════════════════════════════════════════════
# 4. BUNDLE CONFIGURATION ISSUES (BC-001 through BC-018)
# Missing or incorrect bundler configuration
# ═══════════════════════════════════════════════════════════════════════════

declare -a BUNDLEPHOBIA_CONFIG_PATTERNS=()

BUNDLEPHOBIA_CONFIG_PATTERNS+=(
  # Missing splitChunks — webpack
  'PLACEHOLDER_NO_SPLITCHUNKS|medium|BC-001|No webpack splitChunks configuration — all code in one bundle|Add optimization.splitChunks to separate vendor code'

  # No code splitting / dynamic imports
  'PLACEHOLDER_NO_CODE_SPLITTING|medium|BC-002|No dynamic imports detected — missing code splitting for routes|Use import() for route-based code splitting'

  # Missing minification
  'minimize:[[:space:]]*false|high|BC-003|Minification explicitly disabled — bundles will be large|Set minimize: true for production builds'

  # Source maps in production
  'devtool:[[:space:]]*["\x27]source-map["\x27]|medium|BC-004|Full source maps configured — may ship to production|Use hidden-source-map or nosources-source-map for production'
  'devtool:[[:space:]]*["\x27]eval["\x27]|high|BC-005|eval devtool in config — development-only, insecure in production|Use hidden-source-map for production builds'

  # No bundle analyzer configured
  'PLACEHOLDER_NO_ANALYZER|low|BC-006|No bundle analyzer configured — cannot track bundle size|Add webpack-bundle-analyzer or @next/bundle-analyzer for visibility'

  # Missing externals for server-side
  'PLACEHOLDER_NO_EXTERNALS|medium|BC-007|No externals configured for server/library build|Add externals to exclude node_modules from server bundles'

  # target not set for node
  'PLACEHOLDER_WRONG_TARGET|low|BC-008|Bundler target may not match deployment environment|Verify target matches deployment: web for browsers, node for server'

  # Very large chunk size hint
  'maxAssetSize:[[:space:]]*[0-9]{7,}|medium|BC-009|Asset size limit set very high (1MB+) — may mask bundle bloat|Set maxAssetSize to 250000 (250KB) or lower for performance'
  'maxEntrypointSize:[[:space:]]*[0-9]{7,}|medium|BC-010|Entrypoint size limit set very high (1MB+)|Set maxEntrypointSize to 500000 (500KB) or lower'

  # No terser or minifier plugin
  'PLACEHOLDER_NO_TERSER|high|BC-011|No minification plugin detected in bundler config|Add terser-webpack-plugin, esbuild minify, or rollup-plugin-terser'

  # output.filename without hash
  'filename:[[:space:]]*["\x27][a-zA-Z]+\.js["\x27]|medium|BC-012|Output filename without content hash — poor caching|Use [name].[contenthash].js for long-term caching'

  # No publicPath configured
  'PLACEHOLDER_NO_PUBLIC_PATH|low|BC-013|No publicPath configured — may cause asset loading issues in production|Set output.publicPath for CDN or deployment path'

  # mode not set to production
  'mode:[[:space:]]*["\x27]development["\x27]|high|BC-014|Bundler mode set to development — no optimizations applied|Set mode: production for production builds'

  # No compression plugin
  'PLACEHOLDER_NO_COMPRESSION|low|BC-015|No compression plugin configured (gzip/brotli)|Add compression-webpack-plugin for pre-compressed assets'

  # Inline runtime chunk not separated
  'PLACEHOLDER_NO_RUNTIME_CHUNK|low|BC-016|Runtime chunk not separated — invalidates vendor cache on changes|Add optimization.runtimeChunk: single for better caching'

  # Missing resolve.alias for lighter alternatives
  'PLACEHOLDER_NO_ALIAS|low|BC-017|No resolve.alias configured — missing opportunity for lighter swaps|Use resolve.alias to swap heavy libraries (e.g., moment -> dayjs)'

  # No CSS extraction
  'PLACEHOLDER_NO_CSS_EXTRACT|medium|BC-018|CSS bundled with JS — no separate CSS extraction|Use MiniCssExtractPlugin or equivalent to extract CSS into separate files'
)

# ═══════════════════════════════════════════════════════════════════════════
# 5. DEPENDENCY HYGIENE (DH-001 through DH-014+)
# Package.json and dependency management issues
# ═══════════════════════════════════════════════════════════════════════════

declare -a BUNDLEPHOBIA_HYGIENE_PATTERNS=()

BUNDLEPHOBIA_HYGIENE_PATTERNS+=(
  # Exact pinned versions (no ^ or ~) — limits auto-patching
  '"[a-zA-Z@][a-zA-Z0-9@/_.-]+":[[:space:]]*"[0-9]+\.[0-9]+\.[0-9]+"[[:space:]]*$|low|DH-001|Dependency pinned to exact version (no ^/~) — prevents auto-patching|Use ^ prefix for minor updates: ^1.2.3 unless exact pinning is intentional'

  # Star version
  '"[a-zA-Z@][a-zA-Z0-9@/_.-]+":[[:space:]]*"\*"|critical|DH-002|Dependency version set to * — completely unpinned|Pin to a specific version range: ^1.0.0 or ~1.0.0'

  # latest tag as version
  '"[a-zA-Z@][a-zA-Z0-9@/_.-]+":[[:space:]]*"latest"|high|DH-003|Dependency pinned to latest — non-reproducible builds|Pin to a specific version range for reproducible builds'

  # DevDependencies misplaced (common patterns)
  '"@types/[a-zA-Z]|high|DH-004|TypeScript @types package may be in production dependencies|Move @types/* packages to devDependencies'

  # eslint in production deps
  '"eslint"[[:space:]]*:[[:space:]]*"[^"]*"[[:space:]]*$|high|DH-005|eslint in production dependencies — dev tool only|Move eslint and plugins to devDependencies'

  # prettier in production deps
  '"prettier"[[:space:]]*:[[:space:]]*"[^"]*"[[:space:]]*$|medium|DH-006|prettier in production dependencies — dev tool only|Move prettier to devDependencies'

  # test framework in production deps
  '"jest"[[:space:]]*:[[:space:]]*"|"mocha"[[:space:]]*:[[:space:]]*"|"vitest"[[:space:]]*:[[:space:]]*"|high|DH-007|Test framework in production dependencies|Move test frameworks (jest, mocha, vitest) to devDependencies'

  # storybook in production deps
  '"@storybook/[a-zA-Z]|medium|DH-008|Storybook packages in production dependencies|Move @storybook/* packages to devDependencies'

  # Missing browserslist
  'PLACEHOLDER_NO_BROWSERSLIST|low|DH-009|No browserslist configuration — may include unnecessary polyfills|Add browserslist field to package.json or create .browserslistrc'

  # No engines field
  'PLACEHOLDER_NO_ENGINES|low|DH-010|No engines field in package.json — Node.js version not specified|Add engines.node to specify minimum Node.js version for proper polyfilling'

  # Missing sideEffects field
  'PLACEHOLDER_NO_SIDE_EFFECTS|medium|DH-011|No sideEffects field in package.json — hinders tree-shaking|Add "sideEffects": false (or array of files with side effects) to package.json'

  # webpack/bundler in production deps
  '"webpack"[[:space:]]*:[[:space:]]*"[^"]*"[[:space:]]*$|high|DH-012|webpack in production dependencies — build tool only|Move webpack and plugins to devDependencies'

  # babel in production deps
  '"@babel/core"[[:space:]]*:[[:space:]]*"|"babel-core"[[:space:]]*:[[:space:]]*"|high|DH-013|Babel in production dependencies — build tool only|Move @babel/* packages to devDependencies'

  # husky/lint-staged in production deps
  '"husky"[[:space:]]*:[[:space:]]*"|"lint-staged"[[:space:]]*:[[:space:]]*"|medium|DH-014|Git hook tools in production dependencies|Move husky and lint-staged to devDependencies'
)

# ═══════════════════════════════════════════════════════════════════════════
# Utility functions
# ═══════════════════════════════════════════════════════════════════════════

# Get total pattern count across all categories
bundlephobia_pattern_count() {
  local count=0
  count=$((count + ${#BUNDLEPHOBIA_OVERSIZED_PATTERNS[@]}))
  count=$((count + ${#BUNDLEPHOBIA_DUPLICATE_PATTERNS[@]}))
  count=$((count + ${#BUNDLEPHOBIA_TREESHAKE_PATTERNS[@]}))
  count=$((count + ${#BUNDLEPHOBIA_CONFIG_PATTERNS[@]}))
  count=$((count + ${#BUNDLEPHOBIA_HYGIENE_PATTERNS[@]}))
  echo "$count"
}

# List patterns by category
bundlephobia_list_patterns() {
  local filter_type="${1:-all}"
  local -n _patterns_ref

  case "$filter_type" in
    OVERSIZED)   _patterns_ref=BUNDLEPHOBIA_OVERSIZED_PATTERNS ;;
    DUPLICATE)   _patterns_ref=BUNDLEPHOBIA_DUPLICATE_PATTERNS ;;
    TREESHAKE)   _patterns_ref=BUNDLEPHOBIA_TREESHAKE_PATTERNS ;;
    CONFIG)      _patterns_ref=BUNDLEPHOBIA_CONFIG_PATTERNS ;;
    HYGIENE)     _patterns_ref=BUNDLEPHOBIA_HYGIENE_PATTERNS ;;
    all)
      bundlephobia_list_patterns "OVERSIZED"
      bundlephobia_list_patterns "DUPLICATE"
      bundlephobia_list_patterns "TREESHAKE"
      bundlephobia_list_patterns "CONFIG"
      bundlephobia_list_patterns "HYGIENE"
      return
      ;;
    *)
      echo "Unknown category: $filter_type"
      return 1
      ;;
  esac

  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
    # Skip placeholder patterns
    [[ "$regex" == PLACEHOLDER_* ]] && continue
    printf "%-8s %-8s %s\n" "$check_id" "$severity" "$description"
  done
}

# Get patterns array name for a file type
get_patterns_for_file_type() {
  local file_type="$1"
  case "$file_type" in
    source)      echo "BUNDLEPHOBIA_TREESHAKE_PATTERNS" ;;
    package)     echo "BUNDLEPHOBIA_OVERSIZED_PATTERNS" ;;
    config)      echo "BUNDLEPHOBIA_CONFIG_PATTERNS" ;;
    *)           echo "" ;;
  esac
}

# Severity to numeric points for scoring
severity_to_points() {
  case "$1" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo 8 ;;
    low)      echo 3 ;;
    *)        echo 0 ;;
  esac
}
