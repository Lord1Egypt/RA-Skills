import { cmdPublish } from '/Users/abinash/.nvm/versions/node/v24.9.0/lib/node_modules/clawhub/dist/cli/commands/publish.js';
cmdPublish({ workdir: process.cwd(), dir: 'skills' }, '.', { slug: 'eonik', version: '1.0.0', name: 'eonik' }).catch(console.error);
