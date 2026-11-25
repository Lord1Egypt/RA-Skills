import {realpathSync} from 'node:fs';
import {fileURLToPath} from 'node:url';

// Node resolves module symlinks, while argv[1] can retain the user's alias.
export function isCLIEntry(moduleURL,entry=process.argv[1]){
 if(!entry)return false;
 try{return realpathSync(entry)===realpathSync(fileURLToPath(moduleURL))}
 catch{return false}
}
