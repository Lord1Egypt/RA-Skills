import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { chmod, copyFile, mkdir, mkdtemp, readFile, rm, stat, symlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { promisify } from 'node:util';
import Database from 'better-sqlite3';

const exec = promisify(execFile);

test('Apple Contacts sync works with a basic schema and exports extra fields only after opt-in', async (t) => {
  const fixture = await mkdtemp(join(tmpdir(), 'amber-contacts-'));
  t.after(() => rm(fixture, { recursive: true, force: true }));
  const addressBook = join(fixture, 'Library', 'Application Support', 'AddressBook');
  await mkdir(addressBook, { recursive: true });
  const scripts = join(fixture, 'scripts');
  await mkdir(scripts);
  await writeFile(join(fixture, 'package.json'), '{"type":"module"}');
  await symlink(new URL('../node_modules/', import.meta.url), join(fixture, 'node_modules'), 'dir');
  const script = join(scripts, 'sync-contacts.js');
  await copyFile(new URL('../scripts/sync-contacts.js', import.meta.url), script);
  await copyFile(new URL('../write-private-file.js', import.meta.url), join(fixture, 'write-private-file.js'));
  const cachePath = join(fixture, 'contacts-cache.json');

  const db = new Database(join(addressBook, 'AddressBook-v22.abcddb'));
  try {
    db.exec(`
      CREATE TABLE ZABCDRECORD (Z_PK INTEGER PRIMARY KEY, ZFIRSTNAME TEXT, ZLASTNAME TEXT);
      CREATE TABLE ZABCDPHONENUMBER (ZOWNER INTEGER, ZFULLNUMBER TEXT, ZLABEL TEXT);
      INSERT INTO ZABCDRECORD VALUES (1, 'Alex', 'Example');
      INSERT INTO ZABCDPHONENUMBER VALUES (1, '+12025550142', 'mobile');
    `);
    async function sync(extended) {
      const { stderr } = await exec(process.execPath, [script], {
        env: { ...process.env, HOME: fixture, AMBER_CONTACTS_EXTENDED: String(extended) },
      });
      assert.equal(stderr, '');
      assert.equal((await stat(cachePath)).mode & 0o777, 0o600);
      const cache = JSON.parse(await readFile(cachePath, 'utf8'));
      assert.equal(cache.count, 1);
      return cache.contacts[0];
    }
    assert.deepEqual(await sync(false), {
      firstName: 'Alex',
      lastName: 'Example',
      phones: [{ number: '+12025550142', label: 'mobile' }],
    });

    db.exec(`
      ALTER TABLE ZABCDRECORD ADD ZNICKNAME TEXT;
      ALTER TABLE ZABCDRECORD ADD ZORGANIZATION TEXT;
      ALTER TABLE ZABCDRECORD ADD ZJOBTITLE TEXT;
      ALTER TABLE ZABCDRECORD ADD ZNOTE TEXT;
      UPDATE ZABCDRECORD SET ZNICKNAME = 'Al', ZORGANIZATION = 'Example Shop',
        ZJOBTITLE = 'Mechanic', ZNOTE = 'Example note';
      CREATE TABLE ZABCDEMAILADDRESS (ZOWNER INTEGER, ZADDRESS TEXT, ZLABEL TEXT);
      CREATE TABLE ZABCDRELATEDNAME (ZOWNER INTEGER, ZNAME TEXT, ZLABEL TEXT);
      CREATE TABLE ZABCDPOSTALADDRESS (ZOWNER INTEGER, ZSTREET TEXT, ZCITY TEXT, ZSTATE TEXT,
        ZZIPCODE TEXT, ZCOUNTRYNAME TEXT, ZLABEL TEXT);
      INSERT INTO ZABCDEMAILADDRESS VALUES (1, 'alex@example.test', 'work');
      INSERT INTO ZABCDRELATEDNAME VALUES (1, 'Jamie', 'friend');
      INSERT INTO ZABCDPOSTALADDRESS VALUES (1, '100 Example Ave', 'Example City', '', '', '', 'work');
    `);
    await chmod(cachePath, 0o644);
    const extended = await sync(true);
    assert.equal(extended.nickname, 'Al');
    assert.equal(extended.organization, 'Example Shop');
    assert.equal(extended.jobTitle, 'Mechanic');
    assert.equal(extended.note, 'Example note');
    assert.deepEqual(extended.emails, [{ address: 'alex@example.test', label: 'work' }]);
    assert.deepEqual(extended.relationships, [{ name: 'Jamie', type: 'friend' }]);
    assert.deepEqual(extended.addresses, [{ full: '100 Example Ave, Example City', label: 'work' }]);
    assert.deepEqual(Object.keys(await sync(false)).sort(), ['firstName', 'lastName', 'phones']);
  } finally {
    db.close();
  }
});
