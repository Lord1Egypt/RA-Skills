import skill from '../index.js';

const mockConfig = {
  baseUrl: 'https://api.odontosoft.com.py',
  apiKey:  'TOKEN_DE_PRUEBA',
};

const ctx = { config: mockConfig };

// Mock global fetch
globalThis.fetch = async (url, opts) => {
  const rutas = {
    '/api/doctores.php':            { id_clinica: 9, total: 1, doctores: [{ id: 1, nombre: 'Dr. Test' }] },
    '/api/turnos_disponibles.php':  { disponibles: ['09:00', '09:30'] },
    '/api/buscar_paciente.php':     { encontrado: true, paciente: { id: 5, nombre: 'Juan' } },
    '/api/agendar_turno.php':       { ok: true, turno_id: 42 },
  };

  const path = Object.keys(rutas).find(r => url.includes(r));
  const body = path ? rutas[path] : { error: 'ruta no encontrada' };

  return {
    ok: !!path,
    status: path ? 200 : 404,
    text: async () => JSON.stringify(body),
  };
};

// ─── Tests ────────────────────────────────────────────────────────────────────

async function run() {
  let ok = 0;
  let fail = 0;

  async function test(nombre, fn) {
    try {
      await fn();
      console.log(`  ✓ ${nombre}`);
      ok++;
    } catch (err) {
      console.error(`  ✗ ${nombre}: ${err.message}`);
      fail++;
    }
  }

  function assert(cond, msg) {
    if (!cond) throw new Error(msg);
  }

  console.log('\nOdontosoft Skill — Tests\n');

  await test('get_doctores devuelve lista', async () => {
    const res = await skill.get_doctores({}, ctx);
    assert(Array.isArray(res.doctores), 'doctores debe ser array');
    assert(res.total === 1, 'total debe ser 1');
  });

  await test('get_turnos_disponibles devuelve slots', async () => {
    const res = await skill.get_turnos_disponibles({ doctor_id: 1, fecha: '2026-03-25' }, ctx);
    assert(Array.isArray(res.disponibles), 'disponibles debe ser array');
  });

  await test('get_turnos_disponibles falla sin parámetros', async () => {
    const res = await skill.get_turnos_disponibles({}, ctx);
    assert(res.error === true, 'debe devolver error');
  });

  await test('buscar_paciente devuelve paciente', async () => {
    const res = await skill.buscar_paciente({ documento: '12345678' }, ctx);
    assert(res.encontrado === true, 'encontrado debe ser true');
  });

  await test('buscar_paciente falla sin documento', async () => {
    const res = await skill.buscar_paciente({}, ctx);
    assert(res.error === true, 'debe devolver error');
  });

  await test('agendar_turno crea turno', async () => {
    const res = await skill.agendar_turno(
      { paciente_id: 5, doctor_id: 1, fecha: '2026-03-25', hora: '09:00', motivo: 'Consulta' },
      ctx
    );
    assert(res.ok === true, 'ok debe ser true');
    assert(res.turno_id === 42, 'turno_id debe ser 42');
  });

  console.log(`\n${ok} pasados · ${fail} fallidos\n`);
  if (fail > 0) process.exit(1);
}

run();
