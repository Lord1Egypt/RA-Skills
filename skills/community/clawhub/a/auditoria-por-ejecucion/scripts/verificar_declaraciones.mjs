// Detector de "veredicto no cableado": afirmaciones que un script, un gate o un archivo de
// estado hacen sobre si mismos y que no sobreviven a una comprobacion.
//
// Nacio de cuatro casos MEDIDOS el mismo dia en este repo, ninguno deles bug del sistema:
// ninguno era un bug de DECLARACION.
//   1. log("LEADS: 4 nuevos") se ejecutaba ANTES del fs_write. Un ReferenceError mataba el
//      proceso y el log ya habia salido: stdout decia exito, el archivo nunca se escribio.
//   2. El detector de comentarios leia a.content de /api/v1/home. Ese campo no existe.
//      Cero silencioso con forma de acierto.
//   3. Un batch de PowerShell leyo mal $LASTEXITCODE y reporto 3 archivos rotos que
//     	node --check daba por buenos. El instrumento mentia, no el codigo.
//   4. state/limites.json afirmaba un post que la plataforma no tenia: bloqueo 4 horas.
//
// Y la misma clase fuera de aqui:
//   alpha-beth-lab  research/validate_corpus.mjs imprime "VERDICT: CORRUPT" y NO tiene ni
//                   una llamada a process.exit. npm run verify:all (cadena &&) pasa entera.
//   Globalcorp      ci.yml:47 y :72 corren pip-audit con "|| true": nunca rompen el build.
//
// Regla que implementa: antes de reportar un exito, pagar el coste de probarlo contra el
// exterior. Todo lo demas es ruido, y el ruido es lo que hace que la gente deje de mirar.
//
// Uso:
//   node scripts\verificar_declaraciones.mjs "<repo>" [--gate "npm run verify:all"] [--json]
//                    [--yes (consentimiento: sin esto el --gate NO se ejecuta)] [--full-env (renuncia al env sanitizado)]
// Los detectores estaticos son solo lectura y corren siempre; solo el gate es ejecucion.
// El env del gate se sanitiza por defecto (sin KEY/TOKEN/SECRET/PASSWORD/CREDENTIAL/BEARER/AUTH).
// Salida: exit 1 si hay hallazgos, 0 si no.

import { spawnSync } from 'node:child_process';
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, extname } from 'node:path';

const argv = process.argv.slice(2);
const AS_JSON = argv.includes('--json');
// El repo es el primer argumento que NO empieza por --. Los valores de los flags se
// consumen aparte: el find anterior cogia "npm run verify:all" como si fuera el repo,
// porque no sabia que era el valor de --gate.
const REPO = argv.find((a) => !a.startsWith('--')) || '.';
const gI = argv.indexOf('--gate');
const GATE = gI >= 0 ? argv[gI + 1] : null;
const SI = argv.includes('--yes');            // consentimiento explicito para el gate
const fullEnv = argv.includes('--full-env');  // renuncia explicita al env sanitizado

const CODIGOS = ['.mjs', '.js', '.cjs', '.ts', '.py', '.go', '.rb', '.sh', '.ps1'];
const findings = [];
const add = (sev, detector, archivo, linea, texto, porQue) =>
  findings.push({ sev, detector, archivo, linea, texto: String(texto).trim().slice(0, 160), porQue });

// ---------------------------------------------------------------- 0. El repo existe
if (!existsSync(REPO)) {
  console.error('NO EXISTE: ' + REPO);
  process.exit(2);
}

// ---------------------------------------------------------------- 1. VEREDICTO NO CABLEADO
// Corre el gate y compara el codigo de salida contra lo que el gate dice de si mismo.
// Esta es la comprobacion cara (ejecuta el gate) y la unica que no se puede hacer leyendo.
function detectorVeredicto() {
  if (!GATE) return;
  if (!SI) {
    console.error(`EJECUCION OMITIDA (dry-run): --gate "${GATE}" exige --yes. Los detectores estaticos siguen operando.`);
    return null;
  }
  const SECRETO = /KEY|TOKEN|SECRET|PASSWORD|PASSWD|CREDENTIAL|BEARER|AUTH/i;
  const envSanitizado = fullEnv ? process.env
    : Object.fromEntries(Object.entries(process.env).filter(([k]) => !SECRETO.test(k)));
  const r = spawnSync(String(GATE), { cwd: REPO, shell: true, encoding: 'utf8', env: envSanitizado, maxBuffer: 64 * 1024 * 1024, timeout: 10 * 60 * 1000 });
  const salida = (r.stdout || '') + (r.stderr || '');
  const code = r.status;

  // Un "FAIL" suelto puede ser un caso negativo de test que PASSA (assertClean throws on a
  // corrupt corpus = PASS). Un "VERDICT: CORRUPT" no puede ser un PASS.
  const NEGATIVOS = [
    { re: /VERDICT:\s*(?!CLEAN)\b[^\n]*(CORRUPT|DO NOT COMPUTE|FAIL)/gi, peso: 3 },
    { re: /^\s*FAIL\b[^\n]*/gim, peso: 1 },
    { re: /\bassertClean\b[^\n]*(throw|fallo)/gi, peso: 1 },
  ];
  let puntos = 0; const pruebas = [];
  for (const { re, peso } of NEGATIVOS) {
    for (const m of salida.matchAll(re)) {
      puntos += peso; pruebas.push(m[0]);
      if (puntos >= 3) break;
    }
  }

  if (code !== 0) add('ALTO', 'veredicto-no-cableado', 'gate', 0, `el gate salio ${code}`, 'El gate fallo. Bien: el codigo de salida esta cableado.');
  else if (puntos >= 3) {
    add('CRITICO', 'veredicto-no-cableado', 'gate', 0,
      `sale 0 pero declara ${puntos >= 3 ? 'veredicto negativo' : 'fallos'}`,
      'Un && y un CI leen esto como aprobado. El veredicto nunca llega al codigo de salida.');
    for (const p of pruebas.slice(0, 5)) add('EVIDENCIA', 'veredicto-no-cableado', 'gate', 0, p, '');
  } else {
    add('OK', 'veredicto-no-cableado', 'gate', 0, `sale 0 y no declara nada negativo`, 'El gate es coherente con su prosa.');
  }
  return salida;
}

// ---------------------------------------------------------------- recorrido
function recorrer(dir, acc = [], prof = 0) {
  if (prof > 4) return acc;
  let entradas; try { entradas = readdirSync(dir); } catch { return acc; }
  for (const e of entradas) {
    if (e === 'node_modules' || e === '.git' || e === 'dist' || e === 'build' || e === '.venv' || e === '__pycache__') continue;
    const p = join(dir, e);
    let st; try { st = statSync(p); } catch { continue; }
    if (st.isDirectory()) recorrer(p, acc, prof + 1);
    else if (CODIGOS.includes(extname(e))) acc.push(p);
  }
  return acc;
}

const archivos = recorrer(REPO);

// ---------------------------------------------------------------- 2..6. Detectores estaticos
const LINEA_DECLARACION = /\b(log|console\.(log|info|warn|error|debug)|print|println)\s*\(/;
const PALABRAS_EXITO = /\b(nuevos?|listo|listo|ok|guardad|saved|publicad|posted|escrito|wrote|done|complet|hecho|enviad|sent)\b/i;
const ESCRITURA = /\b(writeFileSync|writeFile|appendFileSync|writeJsonAtomic|writeAtomic|writeJsonSecure|fs\.(write|append)|\.save\(|\.commit\(|os\.rename)\b/;
const LIMITE_DECLARADO = /\bconst\s+[A-Z0-9_]*(MAX|MIN|LIMIT|TOPE|RATE|THROTTLE|CUOTA|BUDGET)[A-Z0-9_]*\s*=/;

for (const archivo of archivos) {
  let src; try { src = readFileSync(archivo, 'utf8'); } catch { continue; }
  if (/^\s*[\u0085\uFEFF]/.test(src) && src.charCodeAt(0) === 0xFEFF) src = src.slice(1);
  const lineas = src.split(/\r?\n/);
  const rel = archivo.startsWith(REPO) ? archivo.slice(REPO.length).replace(/^[\\/]/, '') : archivo;

  // 2. constante decorativa: declarada y nunca leida en el mismo archivo
  lineas.forEach((l, i) => {
    const m = l.match(LIMITE_DECLARADO);
    if (!m) return;
    const nombre = l.match(/const\s+([A-Z0-9_]+)/)?.[1];
    if (!nombre) return;
    const usos = (src.match(new RegExp('\\b' + nombre + '\\b', 'g')) || []).length;
    if (usos <= 1) add('ALTO', 'constante-decorativa', rel, i + 1, nombre,
      'Se declara como salvaguarda y no la lee nadie: cuenta como proteccion sin proteger.');
  });

  // 3. declaracion antes del efecto
  let ultimaDeclaracion = -1, ultimaEscritura = -1;
  lineas.forEach((l, i) => {
    if (LINEA_DECLARACION.test(l) && PALABRAS_EXITO.test(l)) ultimaDeclaracion = i;
    if (ESCRITURA.test(l)) ultimaEscritura = i;
  });
  if (ultimaDeclaracion > -1 && ultimaEscritura > -1 && ultimaDeclaracion < ultimaEscritura) {
    add('MEDIO', 'declaracion-antes-del-efecto', rel, ultimaDeclaracion + 1,
      lineas[ultimaDeclaracion].trim(),
      'Declara exito ANTES de la escritura. Si el proceso muere entre medias, stdout dice exito y el efecto no ocurrio.');
  }

  // 4. catch vacio
  lineas.forEach((l, i) => {
    if (/catch\s*\([^)]*\)\s*\{\s*\}/.test(l)) add('BAJO', 'catch-vacio', rel, i + 1, l.trim(),
      'Traga el error: un fallo de escritura se ve como "no habia nada que hacer".');
  });

  // 5. comodines
  lineas.forEach((l, i) => {
    if (/\[(TODO|FIXME|XXX|HACK)\]/i.test(l) && !/^\s*(\/\/|\*|#)/.test(l))
      add('BAJO', 'marca-pendiente', rel, i + 1, l.trim(), 'Trabajo declarado como hecho en el codigo.');
    if (/\|\|\s*true\b/.test(l) && /\.ya?ml$|\.yml$|\.sh$|\.ps1$/.test(rel))
      add('ALTO', 'CI-nunca-falla', rel, i + 1, l.trim(), 'Un gate con "|| true" nunca rompe el build: nunca ha approvesado nada.');
  });
}

// ---------------------------------------------------------------- 7. Estado sin reconciliar
// Un archivo de estado que se LEE para decidir y nunca se compara contra su origen.
for (const archivo of archivos) {
  if (!/state[\\/].*\.json$/.test(archivo)) continue;
  const rel = archivo.slice(REPO.length).replace(/^[\\/]/, '');
  let src; try { src = readFileSync(archivo, 'utf8'); } catch { continue; }
  const quienLoLee = [];
  for (const otro of archivos) {
    if (otro === archivo) continue;
    let s2; try { s2 = readFileSync(otro, 'utf8'); } catch { continue; }
    const base = otro.split(/[\\/]/).pop();
    if (base && s2.includes(base)) quienLoLee.push(base);
  }
  const reconcilia = quienLoLee.some((q) => {
    let s2; try { s2 = readFileSync(join(REPO, 'scripts', q), 'utf8'); } catch { return false; }
    return /reconcili|sync|verific|contrast|contra|remote|API|\/api\//i.test(s2);
  });
  if (quienLoLee.length && !reconcilia)
    add('MEDIO', 'estado-sin-reconciliar', rel, 0, `lo leen ${quienLoLee.length} archivo(s)`,
      'Un estado local sin reconciliacion bloquea cuando no reflects la realidad: no falla, bloquea.');
}

const salidaGate = detectorVeredicto();

// ---------------------------------------------------------------- informe
const porDetector = {};
for (const f of findings) (porDetector[f.detector] ||= []).push(f);
const fallos = findings.filter((f) => f.sev === 'CRITICO' || f.sev === 'ALTO').length;

if (AS_JSON) {
  console.log(JSON.stringify({ repo: REPO, gate: GATE || null, fallos, total: findings.length, porDetector, findings }, null, 2));
} else {
  console.log('=== VEREDICTO NO CABLEADO ===');
  console.log('repo:   ' + REPO);
  console.log('gate:   ' + (GATE ? (SI ? GATE : GATE + ' (OMITIDO: dry-run, sin --yes)') : '(ninguno: los detectores estaticos siguen operando)'));
  console.log('archivos recorridos: ' + archivos.length);
  console.log('');
  const ORDEN = ['CRITICO', 'ALTO', 'MEDIO', 'BAJO', 'EVIDENCIA', 'OK'];
  for (const sev of ORDEN) {
    const lista = findings.filter((f) => f.sev === sev);
    if (!lista.length) continue;
    console.log('-- ' + sev + ' (' + lista.length + ')');
    for (const f of lista.slice(0, 25))
      console.log(`  [${f.detector}] ${f.archivo}${f.linea ? ':' + f.linea : ''} — ${f.texto}${f.porQue ? '\n      ' + f.porQue : ''}`);
    if (lista.length > 25) console.log('  ... y ' + (lista.length - 25) + ' mas');
    console.log('');
  }
  const vered = porDetector['veredicto-no-cableado'] || [];
  const coherente = vered.find((f) => f.sev === 'OK');
  if (coherente) console.log('GATE: el codigo de salida y la prosa coinciden.');
  if (salidaGate && /VERDICT/i.test(salidaGate)) {
    const m = salidaGate.match(/VERDICT:.*/i);
    if (m) console.log('Lo que el gate dijo de si mismo: ' + m[0]);
  }
  console.log(fallos ? 'VEREDICTO: ' + fallos + ' hallazgo(s) de severidad alta o critica' : 'VEREDICTO: ninguna afirmacion sin cablear');
  console.log('Recordatorio: esto no mira si el codigo hace lo que dice que hace. Solo si lo que');
  console.log('declara se sostiene cuando se le quita el efecto.');
}

process.exit(fallos ? 1 : 0);