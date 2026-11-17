// Auditoría de un repositorio externo. Responde una sola pregunta: "¿el gate de este repo
// le está mintiendo a quien lo ejecuta?".
//
//   node scripts\auditar_repo.mjs "D:\ruta\repo" [--cmd "npm run verify:all"] [--json]
//                    [--yes (consentimiento: sin esto NO se ejecuta nada)] [--full-env (renuncia al env sanitizado)]
//
// La lección que justifica este archivo: un gate que IMPRIME un veredicto negativo pero
// sale con código 0 es peor que no tener gate, porque un `&&` y un CI lo leen como verde.
// Encontrado midiendo alpha-beth-lab: `research/validate_corpus.mjs` imprimía
// "VERDICT: CORRUPT — DO NOT COMPUTE ELS ON THIS" sobre un corpus declarado corrupto,
// no tenía ni una llamada a process.exit, y `npm run verify:all` (cadena de &&) pasaba
// entera con exit 0 mientras el sitio se verificaba encima.
// Regla: se juzga por CÓDIGO DE SALIDA, nunca por la prosa. La prosa se reporta aparte.

import { execFileSync, spawnSync } from 'child_process';
import { existsSync, readFileSync } from 'fs';
import { join, resolve } from 'path';

const argv = process.argv.slice(2);
const flag = (n, d) => { const i = argv.indexOf(n); return i < 0 ? d : argv[i + 1]; };
const asJSON = argv.includes('--json');
const target = resolve(argv.find(a => !a.startsWith('--') && argv[argv.indexOf(a) - 1] !== '--cmd') || '.');
const cmd = flag('--cmd', 'npm run verify:all');
const SI = argv.includes('--yes');            // consentimiento explicito por corrida
const fullEnv = argv.includes('--full-env');  // renuncia explicita al env sanitizado

const out = [];
const say = s => { out.push(s); if (!asJSON) console.log(s); };

// ---------------------------------------------------------------- 0. El repo existe
// Solo exigimos que sea un directorio: el comando a auditar no tiene por que ser npm.
// Este repo no tiene package.json y sin embargo su gate (selfcheck.mjs) si es auditable.
if (!existsSync(target)) {
  say(`NO EXISTE: ${target}`);
  process.exit(2);
}

// ---------------------------------------------------------------- 1. Limites de confianza
// Este script EJECUTA codigo de un repo de terceros. Tres fronteras, en orden:
//   a) Consentimiento: sin --yes no se ejecuta nada (dry-run: plan + exit 0).
//   b) Entorno: el proceso hijo no ve variables que casen con
//      KEY|TOKEN|SECRET|PASSWORD|PASSWD|CREDENTIAL|BEARER|AUTH (--full-env renuncia).
//   c) Contexto: codigo de terceros SOLO en contexto desechable (worktree/contenedor/VM),
//      nunca en una maquina que guarde credenciales.
const SECRETO = /KEY|TOKEN|SECRET|PASSWORD|PASSWD|CREDENTIAL|BEARER|AUTH/i;
const envSanitizado = fullEnv
  ? process.env
  : Object.fromEntries(Object.entries(process.env).filter(([k]) => !SECRETO.test(k)));

if (!SI) {
  say('DRY-RUN: sin --yes no se ejecuta nada.');
  say(`  habria corrido: ${cmd}`);
  say(`  en:            ${target}`);
  say(`  env:           ${fullEnv ? 'COMPLETO (--full-env)' : 'sanitizado (KEY/TOKEN/SECRET/PASSWORD/CREDENTIAL/BEARER/AUTH eliminadas)'}`);
  say('  Codigo de terceros solo en contexto desechable. Repetir con --yes para ejecutar.');
  if (asJSON) say(JSON.stringify({ dryRun: true, target, cmd, env: fullEnv ? 'full' : 'sanitized' }));
  process.exit(0);
}

// ---------------------------------------------------------------- 2. Correr el gate
// spawnSync y no execFileSync: el comando es una shell de npm, y ademas queremos el codigo
// de salida aunque el comando reviente, sin que una excepcion nos impida mirarlo.
const r = spawnSync(cmd, {
  cwd: target, shell: true, encoding: 'utf8', env: envSanitizado,
  maxBuffer: 64 * 1024 * 1024, timeout: 10 * 60 * 1000,
});
const text = `${r.stdout || ''}${r.stderr || ''}`;
const code = r.status;

// ---------------------------------------------------------------- 3. Verdictos en la prosa
// Solo cuenta lo que el propio gate declara sobre si mismo. Un FAIL suelto en la salida de
// un test puede ser un caso negativo que pasa; un "VERDICT: CORRUPT" no.
const NEGATIVOS = [
  [/VERDICT:\s*(?!CLEAN)\b.*(CORRUPT|DO NOT COMPUTE|FAIL)/i, 'el gate declara corrupcion'],
  [/^\s*FAIL\b.*$/im, 'lineas FAIL en la salida del gate'],
  [/\bassertClean\b.*(throw|fallo)/i, 'assertClean lanzo sobre el corpus'],
];

// ---------------------------------------------------------------- 4. El veredicto por codigo de salida
const fallos = [];
if (code === null) fallos.push(`el comando no termino normalmente (signal ${r.signal || 'timeout'})`);
else if (code !== 0) fallos.push(`el gate fallo con codigo ${code}`);

// ---------------------------------------------------------------- 5. El defecto que buscamos
// El gate dijo "no" en la prosa y "si" en el codigo de salida. Un gate en ese estado no es
// un gate: es un documento. Cualquier orquestador que encadene con && leeria verde.
const declaroNo = NEGATIVOS.filter(([re]) => re.test(text)).map(([, d]) => d);
const verdictNoCableado = code === 0 && declaroNo.length > 0;
if (verdictNoCableado) {
  fallos.push(`VEREDICTO NO CABLEADO: el gate salio 0 pero ${declaroNo.join(' y ')}. ` +
    'Un && o un CI leeria esto como aprobado.');
}

// ---------------------------------------------------------------- 6. Salida
const lineas = text.split('\n').filter(l => /FAIL|VERDICT|CORRUPT|assertClean|passed|failed|checks? passed/i.test(l));
say(`repo:    ${target}`);
say(`comando: ${cmd}`);
say(`salida:  ${code === null ? 'sin codigo' : code}`);
if (lineas.length) { say('--- evidencia ---'); lineas.slice(0, 40).forEach(l => say('  ' + l.trim())); }
if (lineas.length > 40) say(`  ... y ${lineas.length - 40} lineas mas`);
say(fallos.length ? `VEREDICTO: LOS GATES NO SON FIABLES\n  - ${fallos.join('\n  - ')}`
  : 'VEREDICTO: los gates son coherentes (codigo de salida y prosa coinciden)');

if (asJSON) say(JSON.stringify({ target, cmd, exitCode: code, verdictNoCableado, fallos, evidencia: lineas.slice(0, 40) }));
process.exit(fallos.length ? 1 : 0);