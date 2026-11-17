// Test del blindaje: consentimiento (--yes), env sanitizado y gate omitido sin --yes.
// Uso: node scripts\test_blindaje.mjs   → exit 0 si los 5 asertos pasan.
import { spawnSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const aqui = dirname(fileURLToPath(import.meta.url));
const auditar = join(aqui, 'auditar_repo.mjs');
const verificar = join(aqui, 'verificar_declaraciones.mjs');
let fallos = 0;
const assert = (cond, nombre, detalle = '') => {
  console.log(`${cond ? 'OK  ' : 'FAIL'} ${nombre}${cond ? '' : ' — ' + detalle}`);
  if (!cond) fallos++;
};

// 1. Sin --yes: auditar_repo NO ejecuta nada (dry-run, exit 0).
let r = spawnSync(process.execPath, [auditar, aqui], { encoding: 'utf8' });
assert(r.status === 0 && /DRY-RUN/.test(r.stdout), 'dry-run: sin --yes no ejecuta nada y sale 0', `status=${r.status} out=${r.stdout.slice(0, 200)}`);

// 2. Con --yes y --full-env NO: el gate NO ve secretos del env.
// ("checks passed" en el marcador: es la clase de linea que el informe imprime como evidencia.)
r = spawnSync(process.execPath, [auditar, aqui, '--yes',
  '--cmd', 'node -e "console.log(\'checks passed SEEN:\'+!!process.env.FAKE_SECRET_TOKEN)"'],
  { encoding: 'utf8', env: { ...process.env, FAKE_SECRET_TOKEN: 'x' } });
assert(/SEEN:false/.test(r.stdout), 'env sanitizado: el gate no ve FAKE_SECRET_TOKEN', r.stdout.slice(0, 300));

// 3. Con --full-env: el gate SI lo ve (renuncia explicita).
r = spawnSync(process.execPath, [auditar, aqui, '--yes', '--full-env',
  '--cmd', 'node -e "console.log(\'checks passed SEEN:\'+!!process.env.FAKE_SECRET_TOKEN)"'],
  { encoding: 'utf8', env: { ...process.env, FAKE_SECRET_TOKEN: 'x' } });
assert(/SEEN:true/.test(r.stdout), '--full-env: renuncia explicita funciona', r.stdout.slice(0, 300));

// 4. verificar_declaraciones con --gate y sin --yes: detectores estaticos corren, gate omitido.
r = spawnSync(process.execPath, [verificar, aqui, '--gate', 'node -e "process.exit(5)"'], { encoding: 'utf8' });
assert(/EJECUCION OMITIDA/.test(r.stderr) && /OMITIDO: dry-run/.test(r.stdout),
  'gate omitido sin --yes (aviso + informe lo declara)', `err=${r.stderr.slice(0, 200)}`);

// 5. Con --yes el gate corre y su exit code se audita (gate que sale 5 → hallazgo ALTO).
r = spawnSync(process.execPath, [verificar, aqui, '--yes', '--gate', 'node -e "process.exit(5)"'], { encoding: 'utf8' });
assert(/el gate salio 5/.test(r.stdout) && r.status === 1,
  'con --yes el gate corre y su exit code se audita', r.stdout.slice(0, 300));

process.exit(fallos ? 1 : 0);
