// Local read-only validation only: no runtime, gateway, provider or dispatch imports.
import fs from 'node:fs';
import path from 'node:path';
import {validateConfig} from './policy.mjs';
import {Inbox} from './inbox.mjs';
import {loadRuleset} from './ruleset.mjs';
import {createPublicKey} from 'node:crypto';
try {
 const root=process.argv[2],c=JSON.parse(fs.readFileSync(path.join(root,'plugin-config.json'),'utf8'));
 validateConfig(c);
 for(const peer of Object.values(c.peers))if(createPublicKey(peer.publicKey).asymmetricKeyType!=='ed25519')throw Error();
 new Inbox(path.join(root,'state/plugin-inbox.json'),{readOnly:true}).read();
 if(c.rulesetFile)loadRuleset(path.join(root,'state/plugin-ruleset.json'));
} catch {process.stderr.write('Invalid plugin recovery state; contents withheld.\n');process.exitCode=1;}
