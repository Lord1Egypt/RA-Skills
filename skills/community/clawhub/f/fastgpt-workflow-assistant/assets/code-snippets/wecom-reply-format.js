// Presentation only: never run this formatter over request bodies, model JSON or saved state.
function formatWecomText(value){
 const text=String(value??'').replace(/\r\n/g,'\n');let fenced=false;
 return text.split('\n').map(line=>{
  if(/^\s*(?:```|~~~)/.test(line)){fenced=!fenced;return line;}
  if(fenced||line.length<=88||/^\s*\|/.test(line))return line;
  const protectedRanges=[...line.matchAll(/https?:\/\/[^\s<>]+|\{\{[^\r\n]*?\}\}|`[^`]*`/g)].map(m=>[m.index,m.index+m[0].length]);
  let out='',quote='',start=0;
  for(let i=0;i<line.length;i++){
   const c=line[i];
   if(quote){if(c===quote)quote='';continue;}
   if(c==='“'||c==='「'||c==='『'||c==='"'){quote=({'“':'”','「':'」','『':'』'})[c]||c;continue;}
   if((c==='。'||c==='；')&&!protectedRanges.some(([a,b])=>i>=a&&i<b)&&i<line.length-1){out+=line.slice(start,i+1)+'\n';start=i+1;}
  }
  return out+line.slice(start);
 }).join('\n');
}
