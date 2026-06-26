(function dartProgram(){function copyProperties(a,b){var s=Object.keys(a)
for(var r=0;r<s.length;r++){var q=s[r]
b[q]=a[q]}}function mixinPropertiesHard(a,b){var s=Object.keys(a)
for(var r=0;r<s.length;r++){var q=s[r]
if(!b.hasOwnProperty(q)){b[q]=a[q]}}}function mixinPropertiesEasy(a,b){Object.assign(b,a)}var z=function(){var s=function(){}
s.prototype={p:{}}
var r=new s()
if(!(Object.getPrototypeOf(r)&&Object.getPrototypeOf(r).p===s.prototype.p))return false
try{if(typeof navigator!="undefined"&&typeof navigator.userAgent=="string"&&navigator.userAgent.indexOf("Chrome/")>=0)return true
if(typeof version=="function"&&version.length==0){var q=version()
if(/^\d+\.\d+\.\d+\.\d+$/.test(q))return true}}catch(p){}return false}()
function inherit(a,b){a.prototype.constructor=a
a.prototype["$i"+a.name]=a
if(b!=null){if(z){Object.setPrototypeOf(a.prototype,b.prototype)
return}var s=Object.create(b.prototype)
copyProperties(a.prototype,s)
a.prototype=s}}function inheritMany(a,b){for(var s=0;s<b.length;s++){inherit(b[s],a)}}function mixinEasy(a,b){mixinPropertiesEasy(b.prototype,a.prototype)
a.prototype.constructor=a}function mixinHard(a,b){mixinPropertiesHard(b.prototype,a.prototype)
a.prototype.constructor=a}function lazy(a,b,c,d){var s=a
a[b]=s
a[c]=function(){if(a[b]===s){a[b]=d()}a[c]=function(){return this[b]}
return a[b]}}function lazyFinal(a,b,c,d){var s=a
a[b]=s
a[c]=function(){if(a[b]===s){var r=d()
if(a[b]!==s){A.jm(b)}a[b]=r}var q=a[b]
a[c]=function(){return q}
return q}}function makeConstList(a,b){if(b!=null)A.Y(a,b)
a.$flags=7
return a}function convertToFastObject(a){function t(){}t.prototype=a
new t()
return a}function convertAllToFastObject(a){for(var s=0;s<a.length;++s){convertToFastObject(a[s])}}var y=0
function instanceTearOffGetter(a,b){var s=null
return a?function(c){if(s===null)s=A.eR(b)
return new s(c,this)}:function(){if(s===null)s=A.eR(b)
return new s(this,null)}}function staticTearOffGetter(a){var s=null
return function(){if(s===null)s=A.eR(a).prototype
return s}}var x=0
function tearOffParameters(a,b,c,d,e,f,g,h,i,j){if(typeof h=="number"){h+=x}return{co:a,iS:b,iI:c,rC:d,dV:e,cs:f,fs:g,fT:h,aI:i||0,nDA:j}}function installStaticTearOff(a,b,c,d,e,f,g,h){var s=tearOffParameters(a,true,false,c,d,e,f,g,h,false)
var r=staticTearOffGetter(s)
a[b]=r}function installInstanceTearOff(a,b,c,d,e,f,g,h,i,j){c=!!c
var s=tearOffParameters(a,false,c,d,e,f,g,h,i,!!j)
var r=instanceTearOffGetter(c,s)
a[b]=r}function setOrUpdateInterceptorsByTag(a){var s=v.interceptorsByTag
if(!s){v.interceptorsByTag=a
return}copyProperties(a,s)}function setOrUpdateLeafTags(a){var s=v.leafTags
if(!s){v.leafTags=a
return}copyProperties(a,s)}function updateTypes(a){var s=v.types
var r=s.length
s.push.apply(s,a)
return r}function updateHolder(a,b){copyProperties(b,a)
return a}var hunkHelpers=function(){var s=function(a,b,c,d,e){return function(f,g,h,i){return installInstanceTearOff(f,g,a,b,c,d,[h],i,e,false)}},r=function(a,b,c,d){return function(e,f,g,h){return installStaticTearOff(e,f,a,b,c,[g],h,d)}}
return{inherit:inherit,inheritMany:inheritMany,mixin:mixinEasy,mixinHard:mixinHard,installStaticTearOff:installStaticTearOff,installInstanceTearOff:installInstanceTearOff,_instance_0u:s(0,0,null,["$0"],0),_instance_1u:s(0,1,null,["$1"],0),_instance_2u:s(0,2,null,["$2"],0),_instance_0i:s(1,0,null,["$0"],0),_instance_1i:s(1,1,null,["$1"],0),_instance_2i:s(1,2,null,["$2"],0),_static_0:r(0,null,["$0"],0),_static_1:r(1,null,["$1"],0),_static_2:r(2,null,["$2"],0),makeConstList:makeConstList,lazy:lazy,lazyFinal:lazyFinal,updateHolder:updateHolder,convertToFastObject:convertToFastObject,updateTypes:updateTypes,setOrUpdateInterceptorsByTag:setOrUpdateInterceptorsByTag,setOrUpdateLeafTags:setOrUpdateLeafTags}}()
function initializeDeferredHunk(a){x=v.types.length
a(hunkHelpers,v,w,$)}var J={
eV(a,b,c,d){return{i:a,p:b,e:c,x:d}},
eS(a){var s,r,q,p,o,n=a[v.dispatchPropertyName]
if(n==null)if($.eT==null){A.j9()
n=a[v.dispatchPropertyName]}if(n!=null){s=n.p
if(!1===s)return n.i
if(!0===s)return a
r=Object.getPrototypeOf(a)
if(s===r)return n.i
if(n.e===r)throw A.c(A.fl("Return interceptor for "+A.m(s(a,n))))}q=a.constructor
if(q==null)p=null
else{o=$.dU
if(o==null)o=$.dU=v.getIsolateTag("_$dart_js")
p=q[o]}if(p!=null)return p
p=A.jf(a)
if(p!=null)return p
if(typeof a=="function")return B.x
s=Object.getPrototypeOf(a)
if(s==null)return B.m
if(s===Object.prototype)return B.m
if(typeof q=="function"){o=$.dU
if(o==null)o=$.dU=v.getIsolateTag("_$dart_js")
Object.defineProperty(q,o,{value:B.h,enumerable:false,writable:true,configurable:true})
return B.h}return B.h},
hw(a,b){if(a<0||a>4294967295)throw A.c(A.cC(a,0,4294967295,"length",null))
return J.hy(new Array(a),b)},
hx(a,b){if(a<0)throw A.c(A.b5("Length must be a non-negative integer: "+a,null))
return A.Y(new Array(a),b.h("x<0>"))},
hy(a,b){var s=A.Y(a,b.h("x<0>"))
s.$flags=1
return s},
fc(a){if(a<256)switch(a){case 9:case 10:case 11:case 12:case 13:case 32:case 133:case 160:return!0
default:return!1}switch(a){case 5760:case 8192:case 8193:case 8194:case 8195:case 8196:case 8197:case 8198:case 8199:case 8200:case 8201:case 8202:case 8232:case 8233:case 8239:case 8287:case 12288:case 65279:return!0
default:return!1}},
hz(a,b){var s,r
for(s=a.length;b<s;){r=a.charCodeAt(b)
if(r!==32&&r!==13&&!J.fc(r))break;++b}return b},
hA(a,b){var s,r,q
for(s=a.length;b>0;b=r){r=b-1
if(!(r<s))return A.u(a,r)
q=a.charCodeAt(r)
if(q!==32&&q!==13&&!J.fc(q))break}return b},
ar(a){if(typeof a=="number"){if(Math.floor(a)==a)return J.bd.prototype
return J.co.prototype}if(typeof a=="string")return J.aQ.prototype
if(a==null)return J.be.prototype
if(typeof a=="boolean")return J.cn.prototype
if(Array.isArray(a))return J.x.prototype
if(typeof a!="object"){if(typeof a=="function")return J.aj.prototype
if(typeof a=="symbol")return J.bi.prototype
if(typeof a=="bigint")return J.bg.prototype
return a}if(a instanceof A.f)return a
return J.eS(a)},
d4(a){if(typeof a=="string")return J.aQ.prototype
if(a==null)return a
if(Array.isArray(a))return J.x.prototype
if(typeof a!="object"){if(typeof a=="function")return J.aj.prototype
if(typeof a=="symbol")return J.bi.prototype
if(typeof a=="bigint")return J.bg.prototype
return a}if(a instanceof A.f)return a
return J.eS(a)},
c9(a){if(a==null)return a
if(Array.isArray(a))return J.x.prototype
if(typeof a!="object"){if(typeof a=="function")return J.aj.prototype
if(typeof a=="symbol")return J.bi.prototype
if(typeof a=="bigint")return J.bg.prototype
return a}if(a instanceof A.f)return a
return J.eS(a)},
P(a,b){if(a==null)return b==null
if(typeof a!="object")return b!=null&&a===b
return J.ar(a).H(a,b)},
he(a,b){if(typeof b==="number")if(Array.isArray(a)||A.jc(a,a[v.dispatchPropertyName]))if(b>>>0===b&&b<a.length)return a[b]
return J.c9(a).i(a,b)},
hf(a,b){return J.c9(a).a6(a,b)},
f1(a,b){return J.c9(a).C(a,b)},
eD(a){return J.ar(a).gA(a)},
hg(a){return J.d4(a).gu(a)},
f2(a){return J.d4(a).gJ(a)},
cb(a){return J.c9(a).gt(a)},
aM(a){return J.d4(a).gn(a)},
hh(a){return J.ar(a).gv(a)},
hi(a,b,c){return J.c9(a).X(a,b,c)},
ah(a){return J.ar(a).j(a)},
eE(a,b){return J.c9(a).aF(a,b)},
cl:function cl(){},
cn:function cn(){},
be:function be(){},
bh:function bh(){},
ak:function ak(){},
cA:function cA(){},
bx:function bx(){},
aj:function aj(){},
bg:function bg(){},
bi:function bi(){},
x:function x(a){this.$ti=a},
cm:function cm(){},
dj:function dj(a){this.$ti=a},
at:function at(a,b,c){var _=this
_.a=a
_.b=b
_.c=0
_.d=null
_.$ti=c},
bf:function bf(){},
bd:function bd(){},
co:function co(){},
aQ:function aQ(){}},A={eH:function eH(){},
hl(a,b,c){if(t.R.b(a))return new A.bI(a,b.h("@<0>").l(c).h("bI<1,2>"))
return new A.au(a,b.h("@<0>").l(c).h("au<1,2>"))},
hB(a){return new A.aw("Field '"+a+"' has not been initialized.")},
eh(a,b,c){return a},
eU(a){var s,r
for(s=$.N.length,r=0;r<s;++r)if(a===$.N[r])return!0
return!1},
hF(a,b,c,d){if(t.R.b(a))return new A.bb(a,b,c.h("@<0>").l(d).h("bb<1,2>"))
return new A.E(a,b,c.h("@<0>").l(d).h("E<1,2>"))},
an:function an(){},
b7:function b7(a,b){this.a=a
this.$ti=b},
au:function au(a,b){this.a=a
this.$ti=b},
bI:function bI(a,b){this.a=a
this.$ti=b},
bF:function bF(){},
a4:function a4(a,b){this.a=a
this.$ti=b},
aw:function aw(a){this.a=a},
ew:function ew(){},
d:function d(){},
R:function R(){},
ay:function ay(a,b,c){var _=this
_.a=a
_.b=b
_.c=0
_.d=null
_.$ti=c},
E:function E(a,b,c){this.a=a
this.b=b
this.$ti=c},
bb:function bb(a,b,c){this.a=a
this.b=b
this.$ti=c},
bm:function bm(a,b,c){var _=this
_.a=null
_.b=a
_.c=b
_.$ti=c},
a6:function a6(a,b,c){this.a=a
this.b=b
this.$ti=c},
U:function U(a,b,c){this.a=a
this.b=b
this.$ti=c},
bz:function bz(a,b,c){this.a=a
this.b=b
this.$ti=c},
aa:function aa(a,b){this.a=a
this.$ti=b},
bA:function bA(a,b){this.a=a
this.$ti=b},
D:function D(){},
c2:function c2(){},
h_(a){var s=v.mangledGlobalNames[a]
if(s!=null)return s
return"minified:"+a},
jc(a,b){var s
if(b!=null){s=b.x
if(s!=null)return s}return t.d.b(a)},
m(a){var s
if(typeof a=="string")return a
if(typeof a=="number"){if(a!==0)return""+a}else if(!0===a)return"true"
else if(!1===a)return"false"
else if(a==null)return"null"
s=J.ah(a)
return s},
bt(a){var s,r=$.fg
if(r==null)r=$.fg=Symbol("identityHashCode")
s=a[r]
if(s==null){s=Math.random()*0x3fffffff|0
a[r]=s}return s},
cB(a){var s,r,q,p
if(a instanceof A.f)return A.M(A.aJ(a),null)
s=J.ar(a)
if(s===B.v||s===B.y||t.cr.b(a)){r=B.i(a)
if(r!=="Object"&&r!=="")return r
q=a.constructor
if(typeof q=="function"){p=q.name
if(typeof p=="string"&&p!=="Object"&&p!=="")return p}}return A.M(A.aJ(a),null)},
hI(a){var s,r,q
if(typeof a=="number"||A.ed(a))return J.ah(a)
if(typeof a=="string")return JSON.stringify(a)
if(a instanceof A.ai)return a.j(0)
s=$.hc()
for(r=0;r<1;++r){q=s[r].bW(a)
if(q!=null)return q}return"Instance of '"+A.cB(a)+"'"},
z(a){var s
if(a<=65535)return String.fromCharCode(a)
if(a<=1114111){s=a-65536
return String.fromCharCode((B.e.aY(s,10)|55296)>>>0,s&1023|56320)}throw A.c(A.cC(a,0,1114111,null,null))},
hH(a){var s=a.$thrownJsError
if(s==null)return null
return A.ag(s)},
fh(a,b){var s
if(a.$thrownJsError==null){s=new Error()
A.w(a,s)
a.$thrownJsError=s
s.stack=b.j(0)}},
u(a,b){if(a==null)J.aM(a)
throw A.c(A.ei(a,b))},
ei(a,b){var s,r="index"
if(!A.fJ(b))return new A.a3(!0,b,r,null)
s=A.L(J.aM(a))
if(b<0||b>=s)return A.fa(b,s,a,r)
return new A.bu(null,null,!0,b,r,"Value not in range")},
c(a){return A.w(a,new Error())},
w(a,b){var s
if(a==null)a=new A.a8()
b.dartException=a
s=A.jn
if("defineProperty" in Object){Object.defineProperty(b,"message",{get:s})
b.name=""}else b.toString=s
return b},
jn(){return J.ah(this.dartException)},
b3(a,b){throw A.w(a,b==null?new Error():b)},
eZ(a,b,c){var s
if(b==null)b=0
if(c==null)c=0
s=Error()
A.b3(A.ik(a,b,c),s)},
ik(a,b,c){var s,r,q,p,o,n,m,l,k
if(typeof b=="string")s=b
else{r="[]=;add;removeWhere;retainWhere;removeRange;setRange;setInt8;setInt16;setInt32;setUint8;setUint16;setUint32;setFloat32;setFloat64".split(";")
q=r.length
p=b
if(p>q){c=p/q|0
p%=q}s=r[p]}o=typeof c=="string"?c:"modify;remove from;add to".split(";")[c]
n=t.j.b(a)?"list":"ByteData"
m=a.$flags|0
l="a "
if((m&4)!==0)k="constant "
else if((m&2)!==0){k="unmodifiable "
l="an "}else k=(m&1)!==0?"fixed-length ":""
return new A.by("'"+s+"': Cannot "+o+" "+l+k+n)},
jl(a){throw A.c(A.aP(a))},
a9(a){var s,r,q,p,o,n
a=A.jj(a.replace(String({}),"$receiver$"))
s=a.match(/\\\$[a-zA-Z]+\\\$/g)
if(s==null)s=A.Y([],t.s)
r=s.indexOf("\\$arguments\\$")
q=s.indexOf("\\$argumentsExpr\\$")
p=s.indexOf("\\$expr\\$")
o=s.indexOf("\\$method\\$")
n=s.indexOf("\\$receiver\\$")
return new A.dw(a.replace(new RegExp("\\\\\\$arguments\\\\\\$","g"),"((?:x|[^x])*)").replace(new RegExp("\\\\\\$argumentsExpr\\\\\\$","g"),"((?:x|[^x])*)").replace(new RegExp("\\\\\\$expr\\\\\\$","g"),"((?:x|[^x])*)").replace(new RegExp("\\\\\\$method\\\\\\$","g"),"((?:x|[^x])*)").replace(new RegExp("\\\\\\$receiver\\\\\\$","g"),"((?:x|[^x])*)"),r,q,p,o,n)},
dx(a){return function($expr$){var $argumentsExpr$="$arguments$"
try{$expr$.$method$($argumentsExpr$)}catch(s){return s.message}}(a)},
fk(a){return function($expr$){try{$expr$.$method$}catch(s){return s.message}}(a)},
eI(a,b){var s=b==null,r=s?null:b.method
return new A.cp(a,r,s?null:b.receiver)},
I(a){var s
if(a==null)return new A.dt(a)
if(a instanceof A.bc){s=a.a
return A.as(a,s==null?A.a0(s):s)}if(typeof a!=="object")return a
if("dartException" in a)return A.as(a,a.dartException)
return A.iW(a)},
as(a,b){if(t.C.b(b))if(b.$thrownJsError==null)b.$thrownJsError=a
return b},
iW(a){var s,r,q,p,o,n,m,l,k,j,i,h,g
if(!("message" in a))return a
s=a.message
if("number" in a&&typeof a.number=="number"){r=a.number
q=r&65535
if((B.e.aY(r,16)&8191)===10)switch(q){case 438:return A.as(a,A.eI(A.m(s)+" (Error "+q+")",null))
case 445:case 5007:A.m(s)
return A.as(a,new A.bs())}}if(a instanceof TypeError){p=$.h2()
o=$.h3()
n=$.h4()
m=$.h5()
l=$.h8()
k=$.h9()
j=$.h7()
$.h6()
i=$.hb()
h=$.ha()
g=p.E(s)
if(g!=null)return A.as(a,A.eI(A.C(s),g))
else{g=o.E(s)
if(g!=null){g.method="call"
return A.as(a,A.eI(A.C(s),g))}else if(n.E(s)!=null||m.E(s)!=null||l.E(s)!=null||k.E(s)!=null||j.E(s)!=null||m.E(s)!=null||i.E(s)!=null||h.E(s)!=null){A.C(s)
return A.as(a,new A.bs())}}return A.as(a,new A.cJ(typeof s=="string"?s:""))}if(a instanceof RangeError){if(typeof s=="string"&&s.indexOf("call stack")!==-1)return new A.bw()
s=function(b){try{return String(b)}catch(f){}return null}(a)
return A.as(a,new A.a3(!1,null,null,typeof s=="string"?s.replace(/^RangeError:\s*/,""):s))}if(typeof InternalError=="function"&&a instanceof InternalError)if(typeof s=="string"&&s==="too much recursion")return new A.bw()
return a},
ag(a){var s
if(a instanceof A.bc)return a.b
if(a==null)return new A.bV(a)
s=a.$cachedTrace
if(s!=null)return s
s=new A.bV(a)
if(typeof a==="object")a.$cachedTrace=s
return s},
eW(a){if(a==null)return J.eD(a)
if(typeof a=="object")return A.bt(a)
return J.eD(a)},
j4(a,b){var s,r,q,p=a.length
for(s=0;s<p;s=q){r=s+1
q=r+1
b.B(0,a[s],a[r])}return b},
iv(a,b,c,d,e,f){t.b.a(a)
switch(A.L(b)){case 0:return a.$0()
case 1:return a.$1(c)
case 2:return a.$2(c,d)
case 3:return a.$3(c,d,e)
case 4:return a.$4(c,d,e,f)}throw A.c(A.hu("Unsupported number of arguments for wrapped closure"))},
c8(a,b){var s=a.$identity
if(!!s)return s
s=A.j1(a,b)
a.$identity=s
return s},
j1(a,b){var s
switch(b){case 0:s=a.$0
break
case 1:s=a.$1
break
case 2:s=a.$2
break
case 3:s=a.$3
break
case 4:s=a.$4
break
default:s=null}if(s!=null)return s.bind(a)
return function(c,d,e){return function(f,g,h,i){return e(c,d,f,g,h,i)}}(a,b,A.iv)},
hq(a2){var s,r,q,p,o,n,m,l,k,j,i=a2.co,h=a2.iS,g=a2.iI,f=a2.nDA,e=a2.aI,d=a2.fs,c=a2.cs,b=d[0],a=c[0],a0=i[b],a1=a2.fT
a1.toString
s=h?Object.create(new A.cF().constructor.prototype):Object.create(new A.aN(null,null).constructor.prototype)
s.$initialize=s.constructor
r=h?function static_tear_off(){this.$initialize()}:function tear_off(a3,a4){this.$initialize(a3,a4)}
s.constructor=r
r.prototype=s
s.$_name=b
s.$_target=a0
q=!h
if(q)p=A.f8(b,a0,g,f)
else{s.$static_name=b
p=a0}s.$S=A.hm(a1,h,g)
s[a]=p
for(o=p,n=1;n<d.length;++n){m=d[n]
if(typeof m=="string"){l=i[m]
k=m
m=l}else k=""
j=c[n]
if(j!=null){if(q)m=A.f8(k,m,g,f)
s[j]=m}if(n===e)o=m}s.$C=o
s.$R=a2.rC
s.$D=a2.dV
return r},
hm(a,b,c){if(typeof a=="number")return a
if(typeof a=="string"){if(b)throw A.c("Cannot compute signature for static tearoff.")
return function(d,e){return function(){return e(this,d)}}(a,A.hj)}throw A.c("Error in functionType of tearoff")},
hn(a,b,c,d){var s=A.f7
switch(b?-1:a){case 0:return function(e,f){return function(){return f(this)[e]()}}(c,s)
case 1:return function(e,f){return function(g){return f(this)[e](g)}}(c,s)
case 2:return function(e,f){return function(g,h){return f(this)[e](g,h)}}(c,s)
case 3:return function(e,f){return function(g,h,i){return f(this)[e](g,h,i)}}(c,s)
case 4:return function(e,f){return function(g,h,i,j){return f(this)[e](g,h,i,j)}}(c,s)
case 5:return function(e,f){return function(g,h,i,j,k){return f(this)[e](g,h,i,j,k)}}(c,s)
default:return function(e,f){return function(){return e.apply(f(this),arguments)}}(d,s)}},
f8(a,b,c,d){if(c)return A.hp(a,b,d)
return A.hn(b.length,d,a,b)},
ho(a,b,c,d){var s=A.f7,r=A.hk
switch(b?-1:a){case 0:throw A.c(new A.cD("Intercepted function with no arguments."))
case 1:return function(e,f,g){return function(){return f(this)[e](g(this))}}(c,r,s)
case 2:return function(e,f,g){return function(h){return f(this)[e](g(this),h)}}(c,r,s)
case 3:return function(e,f,g){return function(h,i){return f(this)[e](g(this),h,i)}}(c,r,s)
case 4:return function(e,f,g){return function(h,i,j){return f(this)[e](g(this),h,i,j)}}(c,r,s)
case 5:return function(e,f,g){return function(h,i,j,k){return f(this)[e](g(this),h,i,j,k)}}(c,r,s)
case 6:return function(e,f,g){return function(h,i,j,k,l){return f(this)[e](g(this),h,i,j,k,l)}}(c,r,s)
default:return function(e,f,g){return function(){var q=[g(this)]
Array.prototype.push.apply(q,arguments)
return e.apply(f(this),q)}}(d,r,s)}},
hp(a,b,c){var s,r
if($.f5==null)$.f5=A.f4("interceptor")
if($.f6==null)$.f6=A.f4("receiver")
s=b.length
r=A.ho(s,c,a,b)
return r},
eR(a){return A.hq(a)},
hj(a,b){return A.e6(v.typeUniverse,A.aJ(a.a),b)},
f7(a){return a.a},
hk(a){return a.b},
f4(a){var s,r,q,p=new A.aN("receiver","interceptor"),o=Object.getOwnPropertyNames(p)
o.$flags=1
s=o
for(o=s.length,r=0;r<o;++r){q=s[r]
if(p[q]===a)return q}throw A.c(A.b5("Field name "+a+" not found.",null))},
j5(a){return v.getIsolateTag(a)},
jH(a,b,c){Object.defineProperty(a,b,{value:c,enumerable:false,writable:true,configurable:true})},
jf(a){var s,r,q,p,o,n=A.C($.fW.$1(a)),m=$.ej[n]
if(m!=null){Object.defineProperty(a,v.dispatchPropertyName,{value:m,enumerable:false,writable:true,configurable:true})
return m.i}s=$.en[n]
if(s!=null)return s
r=v.interceptorsByTag[n]
if(r==null){q=A.a1($.fS.$2(a,n))
if(q!=null){m=$.ej[q]
if(m!=null){Object.defineProperty(a,v.dispatchPropertyName,{value:m,enumerable:false,writable:true,configurable:true})
return m.i}s=$.en[q]
if(s!=null)return s
r=v.interceptorsByTag[q]
n=q}}if(r==null)return null
s=r.prototype
p=n[0]
if(p==="!"){m=A.ev(s)
$.ej[n]=m
Object.defineProperty(a,v.dispatchPropertyName,{value:m,enumerable:false,writable:true,configurable:true})
return m.i}if(p==="~"){$.en[n]=s
return s}if(p==="-"){o=A.ev(s)
Object.defineProperty(Object.getPrototypeOf(a),v.dispatchPropertyName,{value:o,enumerable:false,writable:true,configurable:true})
return o.i}if(p==="+")return A.fX(a,s)
if(p==="*")throw A.c(A.fl(n))
if(v.leafTags[n]===true){o=A.ev(s)
Object.defineProperty(Object.getPrototypeOf(a),v.dispatchPropertyName,{value:o,enumerable:false,writable:true,configurable:true})
return o.i}else return A.fX(a,s)},
fX(a,b){var s=Object.getPrototypeOf(a)
Object.defineProperty(s,v.dispatchPropertyName,{value:J.eV(b,s,null,null),enumerable:false,writable:true,configurable:true})
return b},
ev(a){return J.eV(a,!1,null,!!a.$iJ)},
jh(a,b,c){var s=b.prototype
if(v.leafTags[a]===true)return A.ev(s)
else return J.eV(s,c,null,null)},
j9(){if(!0===$.eT)return
$.eT=!0
A.ja()},
ja(){var s,r,q,p,o,n,m,l
$.ej=Object.create(null)
$.en=Object.create(null)
A.j8()
s=v.interceptorsByTag
r=Object.getOwnPropertyNames(s)
if(typeof window!="undefined"){window
q=function(){}
for(p=0;p<r.length;++p){o=r[p]
n=$.fZ.$1(o)
if(n!=null){m=A.jh(o,s[o],n)
if(m!=null){Object.defineProperty(n,v.dispatchPropertyName,{value:m,enumerable:false,writable:true,configurable:true})
q.prototype=n}}}}for(p=0;p<r.length;++p){o=r[p]
if(/^[A-Za-z_]/.test(o)){l=s[o]
s["!"+o]=l
s["~"+o]=l
s["-"+o]=l
s["+"+o]=l
s["*"+o]=l}}},
j8(){var s,r,q,p,o,n,m=B.n()
m=A.b1(B.o,A.b1(B.p,A.b1(B.j,A.b1(B.j,A.b1(B.q,A.b1(B.r,A.b1(B.t(B.i),m)))))))
if(typeof dartNativeDispatchHooksTransformer!="undefined"){s=dartNativeDispatchHooksTransformer
if(typeof s=="function")s=[s]
if(Array.isArray(s))for(r=0;r<s.length;++r){q=s[r]
if(typeof q=="function")m=q(m)||m}}p=m.getTag
o=m.getUnknownTag
n=m.prototypeForTag
$.fW=new A.ek(p)
$.fS=new A.el(o)
$.fZ=new A.em(n)},
b1(a,b){return a(b)||b},
j3(a,b){var s=b.length,r=v.rttc[""+s+";"+a]
if(r==null)return null
if(s===0)return r
if(s===r.length)return r.apply(null,b)
return r(b)},
jj(a){if(/[[\]{}()*+?.\\^$|]/.test(a))return a.replace(/[[\]{}()*+?.\\^$|]/g,"\\$&")
return a},
b9:function b9(){},
ba:function ba(a,b,c){this.a=a
this.b=b
this.$ti=c},
bP:function bP(a,b){this.a=a
this.$ti=b},
bQ:function bQ(a,b,c){var _=this
_.a=a
_.b=b
_.c=0
_.d=null
_.$ti=c},
bv:function bv(){},
dw:function dw(a,b,c,d,e,f){var _=this
_.a=a
_.b=b
_.c=c
_.d=d
_.e=e
_.f=f},
bs:function bs(){},
cp:function cp(a,b,c){this.a=a
this.b=b
this.c=c},
cJ:function cJ(a){this.a=a},
dt:function dt(a){this.a=a},
bc:function bc(a,b){this.a=a
this.b=b},
bV:function bV(a){this.a=a
this.b=null},
ai:function ai(){},
ce:function ce(){},
cf:function cf(){},
cH:function cH(){},
cF:function cF(){},
aN:function aN(a,b){this.a=a
this.b=b},
cD:function cD(a){this.a=a},
a5:function a5(a){var _=this
_.a=0
_.f=_.e=_.d=_.c=_.b=null
_.r=0
_.$ti=a},
dn:function dn(a,b){var _=this
_.a=a
_.b=b
_.d=_.c=null},
ax:function ax(a,b){this.a=a
this.$ti=b},
bk:function bk(a,b,c,d){var _=this
_.a=a
_.b=b
_.c=c
_.d=null
_.$ti=d},
ek:function ek(a){this.a=a},
el:function el(a){this.a=a},
em:function em(a){this.a=a},
jm(a){throw A.w(new A.aw("Field '"+a+"' has been assigned during initialization."),new Error())},
cM(){var s=new A.dI()
return s.b=s},
dI:function dI(){this.b=null},
hG(a,b,c){var s=new Uint8Array(a,b)
return s},
aF(a,b,c){if(a>>>0!==a||a>=c)throw A.c(A.ei(b,a))},
al:function al(){},
aR:function aR(){},
bp:function bp(){},
cW:function cW(a){this.a=a},
cr:function cr(){},
aS:function aS(){},
bn:function bn(){},
bo:function bo(){},
cs:function cs(){},
ct:function ct(){},
cu:function cu(){},
cv:function cv(){},
cw:function cw(){},
cx:function cx(){},
cy:function cy(){},
bq:function bq(){},
br:function br(){},
bR:function bR(){},
bS:function bS(){},
bT:function bT(){},
bU:function bU(){},
eK(a,b){var s=b.c
return s==null?b.c=A.c_(a,"Z",[b.x]):s},
fi(a){var s=a.w
if(s===6||s===7)return A.fi(a.x)
return s===11||s===12},
hK(a){return a.as},
aI(a){return A.e5(v.typeUniverse,a,!1)},
aG(a1,a2,a3,a4){var s,r,q,p,o,n,m,l,k,j,i,h,g,f,e,d,c,b,a,a0=a2.w
switch(a0){case 5:case 1:case 2:case 3:case 4:return a2
case 6:s=a2.x
r=A.aG(a1,s,a3,a4)
if(r===s)return a2
return A.fz(a1,r,!0)
case 7:s=a2.x
r=A.aG(a1,s,a3,a4)
if(r===s)return a2
return A.fy(a1,r,!0)
case 8:q=a2.y
p=A.b0(a1,q,a3,a4)
if(p===q)return a2
return A.c_(a1,a2.x,p)
case 9:o=a2.x
n=A.aG(a1,o,a3,a4)
m=a2.y
l=A.b0(a1,m,a3,a4)
if(n===o&&l===m)return a2
return A.eM(a1,n,l)
case 10:k=a2.x
j=a2.y
i=A.b0(a1,j,a3,a4)
if(i===j)return a2
return A.fA(a1,k,i)
case 11:h=a2.x
g=A.aG(a1,h,a3,a4)
f=a2.y
e=A.iT(a1,f,a3,a4)
if(g===h&&e===f)return a2
return A.fx(a1,g,e)
case 12:d=a2.y
a4+=d.length
c=A.b0(a1,d,a3,a4)
o=a2.x
n=A.aG(a1,o,a3,a4)
if(c===d&&n===o)return a2
return A.eN(a1,n,c,!0)
case 13:b=a2.x
if(b<a4)return a2
a=a3[b-a4]
if(a==null)return a2
return a
default:throw A.c(A.cd("Attempted to substitute unexpected RTI kind "+a0))}},
b0(a,b,c,d){var s,r,q,p,o=b.length,n=A.e7(o)
for(s=!1,r=0;r<o;++r){q=b[r]
p=A.aG(a,q,c,d)
if(p!==q)s=!0
n[r]=p}return s?n:b},
iU(a,b,c,d){var s,r,q,p,o,n,m=b.length,l=A.e7(m)
for(s=!1,r=0;r<m;r+=3){q=b[r]
p=b[r+1]
o=b[r+2]
n=A.aG(a,o,c,d)
if(n!==o)s=!0
l.splice(r,3,q,p,n)}return s?l:b},
iT(a,b,c,d){var s,r=b.a,q=A.b0(a,r,c,d),p=b.b,o=A.b0(a,p,c,d),n=b.c,m=A.iU(a,n,c,d)
if(q===r&&o===p&&m===n)return b
s=new A.cQ()
s.a=q
s.b=o
s.c=m
return s},
Y(a,b){a[v.arrayRti]=b
return a},
fV(a){var s=a.$S
if(s!=null){if(typeof s=="number")return A.j7(s)
return a.$S()}return null},
jb(a,b){var s
if(A.fi(b))if(a instanceof A.ai){s=A.fV(a)
if(s!=null)return s}return A.aJ(a)},
aJ(a){if(a instanceof A.f)return A.e(a)
if(Array.isArray(a))return A.aq(a)
return A.eP(J.ar(a))},
aq(a){var s=a[v.arrayRti],r=t.w
if(s==null)return r
if(s.constructor!==r.constructor)return r
return s},
e(a){var s=a.$ti
return s!=null?s:A.eP(a)},
eP(a){var s=a.constructor,r=s.$ccache
if(r!=null)return r
return A.it(a,s)},
it(a,b){var s=a instanceof A.ai?Object.getPrototypeOf(Object.getPrototypeOf(a)).constructor:b,r=A.i9(v.typeUniverse,s.name)
b.$ccache=r
return r},
j7(a){var s,r=v.types,q=r[a]
if(typeof q=="string"){s=A.e5(v.typeUniverse,q,!1)
r[a]=s
return s}return q},
j6(a){return A.aH(A.e(a))},
iS(a){var s=a instanceof A.ai?A.fV(a):null
if(s!=null)return s
if(t.bW.b(a))return J.hh(a).a
if(Array.isArray(a))return A.aq(a)
return A.aJ(a)},
aH(a){var s=a.r
return s==null?a.r=new A.e4(a):s},
a2(a){return A.aH(A.e5(v.typeUniverse,a,!1))},
is(a){var s=this
s.b=A.iQ(s)
return s.b(a)},
iQ(a){var s,r,q,p,o
if(a===t.K)return A.iB
if(A.aK(a))return A.iF
s=a.w
if(s===6)return A.iq
if(s===1)return A.fL
if(s===7)return A.iw
r=A.iP(a)
if(r!=null)return r
if(s===8){q=a.x
if(a.y.every(A.aK)){a.f="$i"+q
if(q==="k")return A.iz
if(a===t.m)return A.iy
return A.iE}}else if(s===10){p=A.j3(a.x,a.y)
o=p==null?A.fL:p
return o==null?A.a0(o):o}return A.io},
iP(a){if(a.w===8){if(a===t.S)return A.fJ
if(a===t.i||a===t.o)return A.iA
if(a===t.N)return A.iD
if(a===t.y)return A.ed}return null},
ir(a){var s=this,r=A.im
if(A.aK(s))r=A.ig
else if(s===t.K)r=A.a0
else if(A.b2(s)){r=A.ip
if(s===t.a3)r=A.id
else if(s===t.aD)r=A.a1
else if(s===t.cG)r=A.ib
else if(s===t.ae)r=A.fE
else if(s===t.I)r=A.ic
else if(s===t.b1)r=A.aY}else if(s===t.S)r=A.L
else if(s===t.N)r=A.C
else if(s===t.y)r=A.fD
else if(s===t.o)r=A.ie
else if(s===t.i)r=A.eO
else if(s===t.m)r=A.q
s.a=r
return s.a(a)},
io(a){var s=this
if(a==null)return A.b2(s)
return A.jd(v.typeUniverse,A.jb(a,s),s)},
iq(a){if(a==null)return!0
return this.x.b(a)},
iE(a){var s,r=this
if(a==null)return A.b2(r)
s=r.f
if(a instanceof A.f)return!!a[s]
return!!J.ar(a)[s]},
iz(a){var s,r=this
if(a==null)return A.b2(r)
if(typeof a!="object")return!1
if(Array.isArray(a))return!0
s=r.f
if(a instanceof A.f)return!!a[s]
return!!J.ar(a)[s]},
iy(a){var s=this
if(a==null)return!1
if(typeof a=="object"){if(a instanceof A.f)return!!a[s.f]
return!0}if(typeof a=="function")return!0
return!1},
fK(a){if(typeof a=="object"){if(a instanceof A.f)return t.m.b(a)
return!0}if(typeof a=="function")return!0
return!1},
im(a){var s=this
if(a==null){if(A.b2(s))return a}else if(s.b(a))return a
throw A.w(A.fF(a,s),new Error())},
ip(a){var s=this
if(a==null||s.b(a))return a
throw A.w(A.fF(a,s),new Error())},
fF(a,b){return new A.bY("TypeError: "+A.fp(a,A.M(b,null)))},
fp(a,b){return A.cj(a)+": type '"+A.M(A.iS(a),null)+"' is not a subtype of type '"+b+"'"},
O(a,b){return new A.bY("TypeError: "+A.fp(a,b))},
iw(a){var s=this
return s.x.b(a)||A.eK(v.typeUniverse,s).b(a)},
iB(a){return a!=null},
a0(a){if(a!=null)return a
throw A.w(A.O(a,"Object"),new Error())},
iF(a){return!0},
ig(a){return a},
fL(a){return!1},
ed(a){return!0===a||!1===a},
fD(a){if(!0===a)return!0
if(!1===a)return!1
throw A.w(A.O(a,"bool"),new Error())},
ib(a){if(!0===a)return!0
if(!1===a)return!1
if(a==null)return a
throw A.w(A.O(a,"bool?"),new Error())},
eO(a){if(typeof a=="number")return a
throw A.w(A.O(a,"double"),new Error())},
ic(a){if(typeof a=="number")return a
if(a==null)return a
throw A.w(A.O(a,"double?"),new Error())},
fJ(a){return typeof a=="number"&&Math.floor(a)===a},
L(a){if(typeof a=="number"&&Math.floor(a)===a)return a
throw A.w(A.O(a,"int"),new Error())},
id(a){if(typeof a=="number"&&Math.floor(a)===a)return a
if(a==null)return a
throw A.w(A.O(a,"int?"),new Error())},
iA(a){return typeof a=="number"},
ie(a){if(typeof a=="number")return a
throw A.w(A.O(a,"num"),new Error())},
fE(a){if(typeof a=="number")return a
if(a==null)return a
throw A.w(A.O(a,"num?"),new Error())},
iD(a){return typeof a=="string"},
C(a){if(typeof a=="string")return a
throw A.w(A.O(a,"String"),new Error())},
a1(a){if(typeof a=="string")return a
if(a==null)return a
throw A.w(A.O(a,"String?"),new Error())},
q(a){if(A.fK(a))return a
throw A.w(A.O(a,"JSObject"),new Error())},
aY(a){if(a==null)return a
if(A.fK(a))return a
throw A.w(A.O(a,"JSObject?"),new Error())},
fQ(a,b){var s,r,q
for(s="",r="",q=0;q<a.length;++q,r=", ")s+=r+A.M(a[q],b)
return s},
iL(a,b){var s,r,q,p,o,n,m=a.x,l=a.y
if(""===m)return"("+A.fQ(l,b)+")"
s=l.length
r=m.split(",")
q=r.length-s
for(p="(",o="",n=0;n<s;++n,o=", "){p+=o
if(q===0)p+="{"
p+=A.M(l[n],b)
if(q>=0)p+=" "+r[q];++q}return p+"})"},
fG(a3,a4,a5){var s,r,q,p,o,n,m,l,k,j,i,h,g,f,e,d,c,b,a,a0,a1=", ",a2=null
if(a5!=null){s=a5.length
if(a4==null)a4=A.Y([],t.s)
else a2=a4.length
r=a4.length
for(q=s;q>0;--q)B.a.p(a4,"T"+(r+q))
for(p=t.X,o="<",n="",q=0;q<s;++q,n=a1){m=a4.length
l=m-1-q
if(!(l>=0))return A.u(a4,l)
o=o+n+a4[l]
k=a5[q]
j=k.w
if(!(j===2||j===3||j===4||j===5||k===p))o+=" extends "+A.M(k,a4)}o+=">"}else o=""
p=a3.x
i=a3.y
h=i.a
g=h.length
f=i.b
e=f.length
d=i.c
c=d.length
b=A.M(p,a4)
for(a="",a0="",q=0;q<g;++q,a0=a1)a+=a0+A.M(h[q],a4)
if(e>0){a+=a0+"["
for(a0="",q=0;q<e;++q,a0=a1)a+=a0+A.M(f[q],a4)
a+="]"}if(c>0){a+=a0+"{"
for(a0="",q=0;q<c;q+=3,a0=a1){a+=a0
if(d[q+1])a+="required "
a+=A.M(d[q+2],a4)+" "+d[q]}a+="}"}if(a2!=null){a4.toString
a4.length=a2}return o+"("+a+") => "+b},
M(a,b){var s,r,q,p,o,n,m,l=a.w
if(l===5)return"erased"
if(l===2)return"dynamic"
if(l===3)return"void"
if(l===1)return"Never"
if(l===4)return"any"
if(l===6){s=a.x
r=A.M(s,b)
q=s.w
return(q===11||q===12?"("+r+")":r)+"?"}if(l===7)return"FutureOr<"+A.M(a.x,b)+">"
if(l===8){p=A.iV(a.x)
o=a.y
return o.length>0?p+("<"+A.fQ(o,b)+">"):p}if(l===10)return A.iL(a,b)
if(l===11)return A.fG(a,b,null)
if(l===12)return A.fG(a.x,b,a.y)
if(l===13){n=a.x
m=b.length
n=m-1-n
if(!(n>=0&&n<m))return A.u(b,n)
return b[n]}return"?"},
iV(a){var s=v.mangledGlobalNames[a]
if(s!=null)return s
return"minified:"+a},
ia(a,b){var s=a.tR[b]
while(typeof s=="string")s=a.tR[s]
return s},
i9(a,b){var s,r,q,p,o,n=a.eT,m=n[b]
if(m==null)return A.e5(a,b,!1)
else if(typeof m=="number"){s=m
r=A.c0(a,5,"#")
q=A.e7(s)
for(p=0;p<s;++p)q[p]=r
o=A.c_(a,b,q)
n[b]=o
return o}else return m},
i7(a,b){return A.fB(a.tR,b)},
i6(a,b){return A.fB(a.eT,b)},
e5(a,b,c){var s,r=a.eC,q=r.get(b)
if(q!=null)return q
s=A.fv(A.ft(a,null,b,!1))
r.set(b,s)
return s},
e6(a,b,c){var s,r,q=b.z
if(q==null)q=b.z=new Map()
s=q.get(c)
if(s!=null)return s
r=A.fv(A.ft(a,b,c,!0))
q.set(c,r)
return r},
i8(a,b,c){var s,r,q,p=b.Q
if(p==null)p=b.Q=new Map()
s=c.as
r=p.get(s)
if(r!=null)return r
q=A.eM(a,b,c.w===9?c.y:[c])
p.set(s,q)
return q},
ap(a,b){b.a=A.ir
b.b=A.is
return b},
c0(a,b,c){var s,r,q=a.eC.get(c)
if(q!=null)return q
s=new A.S(null,null)
s.w=b
s.as=c
r=A.ap(a,s)
a.eC.set(c,r)
return r},
fz(a,b,c){var s,r=b.as+"?",q=a.eC.get(r)
if(q!=null)return q
s=A.i4(a,b,r,c)
a.eC.set(r,s)
return s},
i4(a,b,c,d){var s,r,q
if(d){s=b.w
r=!0
if(!A.aK(b))if(!(b===t.a||b===t.T))if(s!==6)r=s===7&&A.b2(b.x)
if(r)return b
else if(s===1)return t.a}q=new A.S(null,null)
q.w=6
q.x=b
q.as=c
return A.ap(a,q)},
fy(a,b,c){var s,r=b.as+"/",q=a.eC.get(r)
if(q!=null)return q
s=A.i2(a,b,r,c)
a.eC.set(r,s)
return s},
i2(a,b,c,d){var s,r
if(d){s=b.w
if(A.aK(b)||b===t.K)return b
else if(s===1)return A.c_(a,"Z",[b])
else if(b===t.a||b===t.T)return t.bc}r=new A.S(null,null)
r.w=7
r.x=b
r.as=c
return A.ap(a,r)},
i5(a,b){var s,r,q=""+b+"^",p=a.eC.get(q)
if(p!=null)return p
s=new A.S(null,null)
s.w=13
s.x=b
s.as=q
r=A.ap(a,s)
a.eC.set(q,r)
return r},
bZ(a){var s,r,q,p=a.length
for(s="",r="",q=0;q<p;++q,r=",")s+=r+a[q].as
return s},
i1(a){var s,r,q,p,o,n=a.length
for(s="",r="",q=0;q<n;q+=3,r=","){p=a[q]
o=a[q+1]?"!":":"
s+=r+p+o+a[q+2].as}return s},
c_(a,b,c){var s,r,q,p=b
if(c.length>0)p+="<"+A.bZ(c)+">"
s=a.eC.get(p)
if(s!=null)return s
r=new A.S(null,null)
r.w=8
r.x=b
r.y=c
if(c.length>0)r.c=c[0]
r.as=p
q=A.ap(a,r)
a.eC.set(p,q)
return q},
eM(a,b,c){var s,r,q,p,o,n
if(b.w===9){s=b.x
r=b.y.concat(c)}else{r=c
s=b}q=s.as+(";<"+A.bZ(r)+">")
p=a.eC.get(q)
if(p!=null)return p
o=new A.S(null,null)
o.w=9
o.x=s
o.y=r
o.as=q
n=A.ap(a,o)
a.eC.set(q,n)
return n},
fA(a,b,c){var s,r,q="+"+(b+"("+A.bZ(c)+")"),p=a.eC.get(q)
if(p!=null)return p
s=new A.S(null,null)
s.w=10
s.x=b
s.y=c
s.as=q
r=A.ap(a,s)
a.eC.set(q,r)
return r},
fx(a,b,c){var s,r,q,p,o,n=b.as,m=c.a,l=m.length,k=c.b,j=k.length,i=c.c,h=i.length,g="("+A.bZ(m)
if(j>0){s=l>0?",":""
g+=s+"["+A.bZ(k)+"]"}if(h>0){s=l>0?",":""
g+=s+"{"+A.i1(i)+"}"}r=n+(g+")")
q=a.eC.get(r)
if(q!=null)return q
p=new A.S(null,null)
p.w=11
p.x=b
p.y=c
p.as=r
o=A.ap(a,p)
a.eC.set(r,o)
return o},
eN(a,b,c,d){var s,r=b.as+("<"+A.bZ(c)+">"),q=a.eC.get(r)
if(q!=null)return q
s=A.i3(a,b,c,r,d)
a.eC.set(r,s)
return s},
i3(a,b,c,d,e){var s,r,q,p,o,n,m,l
if(e){s=c.length
r=A.e7(s)
for(q=0,p=0;p<s;++p){o=c[p]
if(o.w===1){r[p]=o;++q}}if(q>0){n=A.aG(a,b,r,0)
m=A.b0(a,c,r,0)
return A.eN(a,n,m,c!==m)}}l=new A.S(null,null)
l.w=12
l.x=b
l.y=c
l.as=d
return A.ap(a,l)},
ft(a,b,c,d){return{u:a,e:b,r:c,s:[],p:0,n:d}},
fv(a){var s,r,q,p,o,n,m,l=a.r,k=a.s
for(s=l.length,r=0;r<s;){q=l.charCodeAt(r)
if(q>=48&&q<=57)r=A.hW(r+1,q,l,k)
else if((((q|32)>>>0)-97&65535)<26||q===95||q===36||q===124)r=A.fu(a,r,l,k,!1)
else if(q===46)r=A.fu(a,r,l,k,!0)
else{++r
switch(q){case 44:break
case 58:k.push(!1)
break
case 33:k.push(!0)
break
case 59:k.push(A.aC(a.u,a.e,k.pop()))
break
case 94:k.push(A.i5(a.u,k.pop()))
break
case 35:k.push(A.c0(a.u,5,"#"))
break
case 64:k.push(A.c0(a.u,2,"@"))
break
case 126:k.push(A.c0(a.u,3,"~"))
break
case 60:k.push(a.p)
a.p=k.length
break
case 62:A.hY(a,k)
break
case 38:A.hX(a,k)
break
case 63:p=a.u
k.push(A.fz(p,A.aC(p,a.e,k.pop()),a.n))
break
case 47:p=a.u
k.push(A.fy(p,A.aC(p,a.e,k.pop()),a.n))
break
case 40:k.push(-3)
k.push(a.p)
a.p=k.length
break
case 41:A.hV(a,k)
break
case 91:k.push(a.p)
a.p=k.length
break
case 93:o=k.splice(a.p)
A.fw(a.u,a.e,o)
a.p=k.pop()
k.push(o)
k.push(-1)
break
case 123:k.push(a.p)
a.p=k.length
break
case 125:o=k.splice(a.p)
A.i_(a.u,a.e,o)
a.p=k.pop()
k.push(o)
k.push(-2)
break
case 43:n=l.indexOf("(",r)
k.push(l.substring(r,n))
k.push(-4)
k.push(a.p)
a.p=k.length
r=n+1
break
default:throw"Bad character "+q}}}m=k.pop()
return A.aC(a.u,a.e,m)},
hW(a,b,c,d){var s,r,q=b-48
for(s=c.length;a<s;++a){r=c.charCodeAt(a)
if(!(r>=48&&r<=57))break
q=q*10+(r-48)}d.push(q)
return a},
fu(a,b,c,d,e){var s,r,q,p,o,n,m=b+1
for(s=c.length;m<s;++m){r=c.charCodeAt(m)
if(r===46){if(e)break
e=!0}else{if(!((((r|32)>>>0)-97&65535)<26||r===95||r===36||r===124))q=r>=48&&r<=57
else q=!0
if(!q)break}}p=c.substring(b,m)
if(e){s=a.u
o=a.e
if(o.w===9)o=o.x
n=A.ia(s,o.x)[p]
if(n==null)A.b3('No "'+p+'" in "'+A.hK(o)+'"')
d.push(A.e6(s,o,n))}else d.push(p)
return m},
hY(a,b){var s,r=a.u,q=A.fs(a,b),p=b.pop()
if(typeof p=="string")b.push(A.c_(r,p,q))
else{s=A.aC(r,a.e,p)
switch(s.w){case 11:b.push(A.eN(r,s,q,a.n))
break
default:b.push(A.eM(r,s,q))
break}}},
hV(a,b){var s,r,q,p=a.u,o=b.pop(),n=null,m=null
if(typeof o=="number")switch(o){case-1:n=b.pop()
break
case-2:m=b.pop()
break
default:b.push(o)
break}else b.push(o)
s=A.fs(a,b)
o=b.pop()
switch(o){case-3:o=b.pop()
if(n==null)n=p.sEA
if(m==null)m=p.sEA
r=A.aC(p,a.e,o)
q=new A.cQ()
q.a=s
q.b=n
q.c=m
b.push(A.fx(p,r,q))
return
case-4:b.push(A.fA(p,b.pop(),s))
return
default:throw A.c(A.cd("Unexpected state under `()`: "+A.m(o)))}},
hX(a,b){var s=b.pop()
if(0===s){b.push(A.c0(a.u,1,"0&"))
return}if(1===s){b.push(A.c0(a.u,4,"1&"))
return}throw A.c(A.cd("Unexpected extended operation "+A.m(s)))},
fs(a,b){var s=b.splice(a.p)
A.fw(a.u,a.e,s)
a.p=b.pop()
return s},
aC(a,b,c){if(typeof c=="string")return A.c_(a,c,a.sEA)
else if(typeof c=="number"){b.toString
return A.hZ(a,b,c)}else return c},
fw(a,b,c){var s,r=c.length
for(s=0;s<r;++s)c[s]=A.aC(a,b,c[s])},
i_(a,b,c){var s,r=c.length
for(s=2;s<r;s+=3)c[s]=A.aC(a,b,c[s])},
hZ(a,b,c){var s,r,q=b.w
if(q===9){if(c===0)return b.x
s=b.y
r=s.length
if(c<=r)return s[c-1]
c-=r
b=b.x
q=b.w}else if(c===0)return b
if(q!==8)throw A.c(A.cd("Indexed base must be an interface type"))
s=b.y
if(c<=s.length)return s[c-1]
throw A.c(A.cd("Bad index "+c+" for "+b.j(0)))},
jd(a,b,c){var s,r=b.d
if(r==null)r=b.d=new Map()
s=r.get(c)
if(s==null){s=A.v(a,b,null,c,null)
r.set(c,s)}return s},
v(a,b,c,d,e){var s,r,q,p,o,n,m,l,k,j,i
if(b===d)return!0
if(A.aK(d))return!0
s=b.w
if(s===4)return!0
if(A.aK(b))return!1
if(b.w===1)return!0
r=s===13
if(r)if(A.v(a,c[b.x],c,d,e))return!0
q=d.w
p=t.a
if(b===p||b===t.T){if(q===7)return A.v(a,b,c,d.x,e)
return d===p||d===t.T||q===6}if(d===t.K){if(s===7)return A.v(a,b.x,c,d,e)
return s!==6}if(s===7){if(!A.v(a,b.x,c,d,e))return!1
return A.v(a,A.eK(a,b),c,d,e)}if(s===6)return A.v(a,p,c,d,e)&&A.v(a,b.x,c,d,e)
if(q===7){if(A.v(a,b,c,d.x,e))return!0
return A.v(a,b,c,A.eK(a,d),e)}if(q===6)return A.v(a,b,c,p,e)||A.v(a,b,c,d.x,e)
if(r)return!1
p=s!==11
if((!p||s===12)&&d===t.b)return!0
o=s===10
if(o&&d===t.cY)return!0
if(q===12){if(b===t.L)return!0
if(s!==12)return!1
n=b.y
m=d.y
l=n.length
if(l!==m.length)return!1
c=c==null?n:n.concat(c)
e=e==null?m:m.concat(e)
for(k=0;k<l;++k){j=n[k]
i=m[k]
if(!A.v(a,j,c,i,e)||!A.v(a,i,e,j,c))return!1}return A.fI(a,b.x,c,d.x,e)}if(q===11){if(b===t.L)return!0
if(p)return!1
return A.fI(a,b,c,d,e)}if(s===8){if(q!==8)return!1
return A.ix(a,b,c,d,e)}if(o&&q===10)return A.iC(a,b,c,d,e)
return!1},
fI(a3,a4,a5,a6,a7){var s,r,q,p,o,n,m,l,k,j,i,h,g,f,e,d,c,b,a,a0,a1,a2
if(!A.v(a3,a4.x,a5,a6.x,a7))return!1
s=a4.y
r=a6.y
q=s.a
p=r.a
o=q.length
n=p.length
if(o>n)return!1
m=n-o
l=s.b
k=r.b
j=l.length
i=k.length
if(o+j<n+i)return!1
for(h=0;h<o;++h){g=q[h]
if(!A.v(a3,p[h],a7,g,a5))return!1}for(h=0;h<m;++h){g=l[h]
if(!A.v(a3,p[o+h],a7,g,a5))return!1}for(h=0;h<i;++h){g=l[m+h]
if(!A.v(a3,k[h],a7,g,a5))return!1}f=s.c
e=r.c
d=f.length
c=e.length
for(b=0,a=0;a<c;a+=3){a0=e[a]
for(;;){if(b>=d)return!1
a1=f[b]
b+=3
if(a0<a1)return!1
a2=f[b-2]
if(a1<a0){if(a2)return!1
continue}g=e[a+1]
if(a2&&!g)return!1
g=f[b-1]
if(!A.v(a3,e[a+2],a7,g,a5))return!1
break}}while(b<d){if(f[b+1])return!1
b+=3}return!0},
ix(a,b,c,d,e){var s,r,q,p,o,n=b.x,m=d.x
while(n!==m){s=a.tR[n]
if(s==null)return!1
if(typeof s=="string"){n=s
continue}r=s[m]
if(r==null)return!1
q=r.length
p=q>0?new Array(q):v.typeUniverse.sEA
for(o=0;o<q;++o)p[o]=A.e6(a,b,r[o])
return A.fC(a,p,null,c,d.y,e)}return A.fC(a,b.y,null,c,d.y,e)},
fC(a,b,c,d,e,f){var s,r=b.length
for(s=0;s<r;++s)if(!A.v(a,b[s],d,e[s],f))return!1
return!0},
iC(a,b,c,d,e){var s,r=b.y,q=d.y,p=r.length
if(p!==q.length)return!1
if(b.x!==d.x)return!1
for(s=0;s<p;++s)if(!A.v(a,r[s],c,q[s],e))return!1
return!0},
b2(a){var s=a.w,r=!0
if(!(a===t.a||a===t.T))if(!A.aK(a))if(s!==6)r=s===7&&A.b2(a.x)
return r},
aK(a){var s=a.w
return s===2||s===3||s===4||s===5||a===t.X},
fB(a,b){var s,r,q=Object.keys(b),p=q.length
for(s=0;s<p;++s){r=q[s]
a[r]=b[r]}},
e7(a){return a>0?new Array(a):v.typeUniverse.sEA},
S:function S(a,b){var _=this
_.a=a
_.b=b
_.r=_.f=_.d=_.c=null
_.w=0
_.as=_.Q=_.z=_.y=_.x=null},
cQ:function cQ(){this.c=this.b=this.a=null},
e4:function e4(a){this.a=a},
cP:function cP(){},
bY:function bY(a){this.a=a},
hN(){var s,r,q
if(self.scheduleImmediate!=null)return A.iY()
if(self.MutationObserver!=null&&self.document!=null){s={}
r=self.document.createElement("div")
q=self.document.createElement("span")
s.a=null
new self.MutationObserver(A.c8(new A.dD(s),1)).observe(r,{childList:true})
return new A.dC(s,r,q)}else if(self.setImmediate!=null)return A.iZ()
return A.j_()},
hO(a){self.scheduleImmediate(A.c8(new A.dE(t.M.a(a)),0))},
hP(a){self.setImmediate(A.c8(new A.dF(t.M.a(a)),0))},
hQ(a){t.M.a(a)
A.i0(0,a)},
i0(a,b){var s=new A.e2()
s.bf(a,b)
return s},
d0(a){return new A.bB(new A.i($.h,a.h("i<0>")),a.h("bB<0>"))},
d_(a,b){a.$2(0,null)
b.b=!0
return b.a},
aE(a,b){A.ih(a,b)},
cZ(a,b){b.V(a)},
cY(a,b){b.a7(A.I(a),A.ag(a))},
ih(a,b){var s,r,q=new A.e8(b),p=new A.e9(b)
if(a instanceof A.i)a.b_(q,p,t.z)
else{s=t.z
if(a instanceof A.i)a.b9(q,p,s)
else{r=new A.i($.h,t._)
r.a=8
r.c=a
r.b_(q,p,s)}}},
d3(a){var s=function(b,c){return function(d,e){while(true){try{b(d,e)
break}catch(r){e=r
d=c}}}}(a,1)
return $.h.aB(new A.ef(s),t.H,t.S,t.z)},
d7(a){var s
if(t.C.b(a)){s=a.gO()
if(s!=null)return s}return B.d},
f9(a,b){var s
b.a(a)
s=new A.i($.h,b.h("i<0>"))
s.K(a)
return s},
iu(a,b){if($.h===B.b)return null
return null},
fH(a,b){if($.h!==B.b)A.iu(a,b)
if(b==null)if(t.C.b(a)){b=a.gO()
if(b==null){A.fh(a,B.d)
b=B.d}}else b=B.d
else if(t.C.b(a))A.fh(a,b)
return new A.A(a,b)},
eL(a,b,c){var s,r,q,p,o={},n=o.a=a
for(s=t._;r=n.a,(r&4)!==0;n=a){a=s.a(n.c)
o.a=a}if(n===b){s=A.hL()
b.R(new A.A(new A.a3(!0,n,null,"Cannot complete a future with itself"),s))
return}q=b.a&1
s=n.a=r|q
if((s&24)===0){p=t.F.a(b.c)
b.a=b.a&1|4
b.c=n
n.aT(p)
return}if(!c)if(b.c==null)n=(s&16)===0||q!==0
else n=!1
else n=!0
if(n){p=b.T()
b.a2(o.a)
A.aB(b,p)
return}b.a^=2
A.b_(null,null,b.b,t.M.a(new A.dN(o,b)))},
aB(a,b){var s,r,q,p,o,n,m,l,k,j,i,h,g,f,e,d={},c=d.a=a
for(s=t.n,r=t.F;;){q={}
p=c.a
o=(p&16)===0
n=!o
if(b==null){if(n&&(p&1)===0){m=s.a(c.c)
A.c7(m.a,m.b)}return}q.a=b
l=b.a
for(c=b;l!=null;c=l,l=k){c.a=null
A.aB(d.a,c)
q.a=l
k=l.a}p=d.a
j=p.c
q.b=n
q.c=j
if(o){i=c.c
i=(i&1)!==0||(i&15)===8}else i=!0
if(i){h=c.b.b
if(n){p=p.b===h
p=!(p||p)}else p=!1
if(p){s.a(j)
A.c7(j.a,j.b)
return}g=$.h
if(g!==h)$.h=h
else g=null
c=c.c
if((c&15)===8)new A.dR(q,d,n).$0()
else if(o){if((c&1)!==0)new A.dQ(q,j).$0()}else if((c&2)!==0)new A.dP(d,q).$0()
if(g!=null)$.h=g
c=q.c
if(c instanceof A.i){p=q.a.$ti
p=p.h("Z<2>").b(c)||!p.y[1].b(c)}else p=!1
if(p){f=q.a.b
if((c.a&24)!==0){e=r.a(f.c)
f.c=null
b=f.a5(e)
f.a=c.a&30|f.a&1
f.c=c.c
d.a=c
continue}else A.eL(c,f,!0)
return}}f=q.a.b
e=r.a(f.c)
f.c=null
b=f.a5(e)
c=q.b
p=q.c
if(!c){f.$ti.c.a(p)
f.a=8
f.c=p}else{s.a(p)
f.a=f.a&1|16
f.c=p}d.a=f
c=f}},
iM(a,b){var s
if(t.Q.b(a))return b.aB(a,t.z,t.K,t.l)
s=t.v
if(s.b(a))return s.a(a)
throw A.c(A.f3(a,"onError",u.c))},
iH(){var s,r
for(s=$.aZ;s!=null;s=$.aZ){$.c6=null
r=s.b
$.aZ=r
if(r==null)$.c5=null
s.a.$0()}},
iR(){$.eQ=!0
try{A.iH()}finally{$.c6=null
$.eQ=!1
if($.aZ!=null)$.f0().$1(A.fU())}},
fR(a){var s=new A.cK(a),r=$.c5
if(r==null){$.aZ=$.c5=s
if(!$.eQ)$.f0().$1(A.fU())}else $.c5=r.b=s},
iO(a){var s,r,q,p=$.aZ
if(p==null){A.fR(a)
$.c6=$.c5
return}s=new A.cK(a)
r=$.c6
if(r==null){s.b=p
$.aZ=$.c6=s}else{q=r.b
s.b=q
$.c6=r.b=s
if(q==null)$.c5=s}},
eY(a){var s=null,r=$.h
if(B.b===r){A.b_(s,s,B.b,a)
return}A.b_(s,s,r,t.M.a(r.b2(a)))},
ju(a,b){return new A.aD(A.eh(a,"stream",t.K),b.h("aD<0>"))},
d2(a){return},
hR(a,b,c,d,e,f){var s,r,q=$.h,p=e?1:0,o=c!=null?32:0
t.p.l(f).h("1(2)").a(b)
s=A.fo(q,c)
r=d==null?A.fT():d
return new A.ac(a,b,s,t.M.a(r),q,p|o,f.h("ac<0>"))},
fo(a,b){if(b==null)b=A.j0()
if(t.e.b(b))return a.aB(b,t.z,t.K,t.l)
if(t.u.b(b))return t.v.a(b)
throw A.c(A.b5("handleError callback must take either an Object (the error), or both an Object (the error) and a StackTrace.",null))},
iJ(a,b){A.c7(a,b)},
iI(){},
c7(a,b){A.iO(new A.ee(a,b))},
fN(a,b,c,d,e){var s,r=$.h
if(r===c)return d.$0()
$.h=c
s=r
try{r=d.$0()
return r}finally{$.h=s}},
fP(a,b,c,d,e,f,g){var s,r=$.h
if(r===c)return d.$1(e)
$.h=c
s=r
try{r=d.$1(e)
return r}finally{$.h=s}},
fO(a,b,c,d,e,f,g,h,i){var s,r=$.h
if(r===c)return d.$2(e,f)
$.h=c
s=r
try{r=d.$2(e,f)
return r}finally{$.h=s}},
b_(a,b,c,d){t.M.a(d)
if(B.b!==c){d=c.b2(d)
d=d}A.fR(d)},
dD:function dD(a){this.a=a},
dC:function dC(a,b,c){this.a=a
this.b=b
this.c=c},
dE:function dE(a){this.a=a},
dF:function dF(a){this.a=a},
e2:function e2(){},
e3:function e3(a,b){this.a=a
this.b=b},
bB:function bB(a,b){this.a=a
this.b=!1
this.$ti=b},
e8:function e8(a){this.a=a},
e9:function e9(a){this.a=a},
ef:function ef(a){this.a=a},
A:function A(a,b){this.a=a
this.b=b},
bD:function bD(a,b){this.a=a
this.$ti=b},
a_:function a_(a,b,c,d,e,f,g){var _=this
_.ay=0
_.CW=_.ch=null
_.w=a
_.a=b
_.b=c
_.c=d
_.d=e
_.e=f
_.r=_.f=null
_.$ti=g},
bE:function bE(){},
bC:function bC(a,b,c){var _=this
_.a=a
_.b=b
_.c=0
_.r=_.e=_.d=null
_.$ti=c},
bG:function bG(){},
ab:function ab(a,b){this.a=a
this.$ti=b},
af:function af(a,b,c,d,e){var _=this
_.a=null
_.b=a
_.c=b
_.d=c
_.e=d
_.$ti=e},
i:function i(a,b){var _=this
_.a=0
_.b=a
_.c=null
_.$ti=b},
dK:function dK(a,b){this.a=a
this.b=b},
dO:function dO(a,b){this.a=a
this.b=b},
dN:function dN(a,b){this.a=a
this.b=b},
dM:function dM(a,b){this.a=a
this.b=b},
dL:function dL(a,b){this.a=a
this.b=b},
dR:function dR(a,b,c){this.a=a
this.b=b
this.c=c},
dS:function dS(a,b){this.a=a
this.b=b},
dT:function dT(a){this.a=a},
dQ:function dQ(a,b){this.a=a
this.b=b},
dP:function dP(a,b){this.a=a
this.b=b},
cK:function cK(a){this.a=a
this.b=null},
a7:function a7(){},
du:function du(a,b){this.a=a
this.b=b},
dv:function dv(a,b){this.a=a
this.b=b},
bW:function bW(){},
e1:function e1(a){this.a=a},
e0:function e0(a){this.a=a},
cL:function cL(){},
aU:function aU(a,b,c,d,e){var _=this
_.a=null
_.b=0
_.c=null
_.d=a
_.e=b
_.f=c
_.r=d
_.$ti=e},
ao:function ao(a,b){this.a=a
this.$ti=b},
ac:function ac(a,b,c,d,e,f,g){var _=this
_.w=a
_.a=b
_.b=c
_.c=d
_.d=e
_.e=f
_.r=_.f=null
_.$ti=g},
az:function az(){},
dH:function dH(a,b,c){this.a=a
this.b=b
this.c=c},
dG:function dG(a){this.a=a},
aX:function aX(){},
ae:function ae(){},
ad:function ad(a,b){this.b=a
this.a=null
this.$ti=b},
bH:function bH(a,b){this.b=a
this.c=b
this.a=null},
cN:function cN(){},
W:function W(a){var _=this
_.a=0
_.c=_.b=null
_.$ti=a},
dY:function dY(a,b){this.a=a
this.b=b},
aV:function aV(a,b){var _=this
_.a=1
_.b=a
_.c=null
_.$ti=b},
aD:function aD(a,b){var _=this
_.a=null
_.b=a
_.c=!1
_.$ti=b},
c1:function c1(){},
cT:function cT(){},
dZ:function dZ(a,b){this.a=a
this.b=b},
e_:function e_(a,b,c){this.a=a
this.b=b
this.c=c},
ee:function ee(a,b){this.a=a
this.b=b},
fq(a,b){var s=a[b]
return s===a?null:s},
fr(a,b,c){if(c==null)a[b]=a
else a[b]=c},
hS(){var s=Object.create(null)
A.fr(s,"<non-identifier-key>",s)
delete s["<non-identifier-key>"]
return s},
hC(a,b){return new A.a5(a.h("@<0>").l(b).h("a5<1,2>"))},
bl(a,b,c){return b.h("@<0>").l(c).h("fe<1,2>").a(A.j4(a,new A.a5(b.h("@<0>").l(c).h("a5<1,2>"))))},
dp(a,b){return new A.a5(a.h("@<0>").l(b).h("a5<1,2>"))},
hD(a,b,c){var s=A.hC(b,c)
a.G(0,new A.dq(s,b,c))
return s},
eJ(a){var s,r
if(A.eU(a))return"{...}"
s=new A.aT("")
try{r={}
B.a.p($.N,a)
s.a+="{"
r.a=!0
a.G(0,new A.dr(r,s))
s.a+="}"}finally{if(0>=$.N.length)return A.u($.N,-1)
$.N.pop()}r=s.a
return r.charCodeAt(0)==0?r:r},
bL:function bL(){},
bO:function bO(a){var _=this
_.a=0
_.e=_.d=_.c=_.b=null
_.$ti=a},
bM:function bM(a,b){this.a=a
this.$ti=b},
bN:function bN(a,b,c){var _=this
_.a=a
_.b=b
_.c=0
_.d=null
_.$ti=c},
dq:function dq(a,b,c){this.a=a
this.b=b
this.c=c},
l:function l(){},
y:function y(){},
dr:function dr(a,b){this.a=a
this.b=b},
iK(a,b){var s,r,q,p=null
try{p=JSON.parse(a)}catch(r){s=A.I(r)
q=String(s)
throw A.c(new A.da(q))}q=A.ea(p)
return q},
ea(a){var s
if(a==null)return null
if(typeof a!="object")return a
if(!Array.isArray(a))return new A.cR(a,Object.create(null))
for(s=0;s<a.length;++s)a[s]=A.ea(a[s])
return a},
fd(a,b,c){return new A.bj(a,b)},
ij(a){return a.c_()},
hT(a,b){return new A.dV(a,[],A.j2())},
hU(a,b,c){var s,r=new A.aT(""),q=A.hT(r,b)
q.ab(a)
s=r.a
return s.charCodeAt(0)==0?s:s},
cR:function cR(a,b){this.a=a
this.b=b
this.c=null},
cS:function cS(a){this.a=a},
cg:function cg(){},
ci:function ci(){},
bj:function bj(a,b){this.a=a
this.b=b},
cq:function cq(a,b){this.a=a
this.b=b},
dk:function dk(){},
dm:function dm(a){this.b=a},
dl:function dl(a){this.a=a},
dW:function dW(){},
dX:function dX(a,b){this.a=a
this.b=b},
dV:function dV(a,b,c){this.c=a
this.a=b
this.b=c},
hs(a,b){a=A.w(a,new Error())
if(a==null)a=A.a0(a)
a.stack=b.j(0)
throw a},
ff(a,b,c,d){var s,r=c?J.hx(a,d):J.hw(a,d)
if(a!==0&&b!=null)for(s=0;s<r.length;++s)r[s]=b
return r},
hE(a,b){var s,r=A.Y([],b.h("x<0>"))
for(s=a.gt(a);s.k();)B.a.p(r,s.gm())
return r},
fj(a,b,c){var s=J.cb(b)
if(!s.k())return a
if(c.length===0){do a+=A.m(s.gm())
while(s.k())}else{a+=A.m(s.gm())
while(s.k())a=a+c+A.m(s.gm())}return a},
hL(){return A.ag(new Error())},
cj(a){if(typeof a=="number"||A.ed(a)||a==null)return J.ah(a)
if(typeof a=="string")return JSON.stringify(a)
return A.hI(a)},
ht(a,b){A.eh(a,"error",t.K)
A.eh(b,"stackTrace",t.l)
A.hs(a,b)},
cd(a){return new A.cc(a)},
b5(a,b){return new A.a3(!1,null,b,a)},
f3(a,b,c){return new A.a3(!0,a,b,c)},
cC(a,b,c,d,e){return new A.bu(b,c,!0,a,d,"Invalid value")},
hJ(a,b,c){if(a>c)throw A.c(A.cC(a,0,c,"start",null))
if(a>b||b>c)throw A.c(A.cC(b,a,c,"end",null))
return b},
fa(a,b,c,d){return new A.ck(b,!0,a,d,"Index out of range")},
fm(a){return new A.by(a)},
fl(a){return new A.cI(a)},
cE(a){return new A.am(a)},
aP(a){return new A.ch(a)},
hu(a){return new A.aA(a)},
hv(a,b,c){var s,r
if(A.eU(a)){if(b==="("&&c===")")return"(...)"
return b+"..."+c}s=A.Y([],t.s)
B.a.p($.N,a)
try{A.iG(a,s)}finally{if(0>=$.N.length)return A.u($.N,-1)
$.N.pop()}r=A.fj(b,t.U.a(s),", ")+c
return r.charCodeAt(0)==0?r:r},
fb(a,b,c){var s,r
if(A.eU(a))return b+"..."+c
s=new A.aT(b)
B.a.p($.N,a)
try{r=s
r.a=A.fj(r.a,a,", ")}finally{if(0>=$.N.length)return A.u($.N,-1)
$.N.pop()}s.a+=c
r=s.a
return r.charCodeAt(0)==0?r:r},
iG(a,b){var s,r,q,p,o,n,m,l=a.gt(a),k=0,j=0
for(;;){if(!(k<80||j<3))break
if(!l.k())return
s=A.m(l.gm())
B.a.p(b,s)
k+=s.length+2;++j}if(!l.k()){if(j<=5)return
if(0>=b.length)return A.u(b,-1)
r=b.pop()
if(0>=b.length)return A.u(b,-1)
q=b.pop()}else{p=l.gm();++j
if(!l.k()){if(j<=4){B.a.p(b,A.m(p))
return}r=A.m(p)
if(0>=b.length)return A.u(b,-1)
q=b.pop()
k+=r.length+2}else{o=l.gm();++j
for(;l.k();p=o,o=n){n=l.gm();++j
if(j>100){for(;;){if(!(k>75&&j>3))break
if(0>=b.length)return A.u(b,-1)
k-=b.pop().length+2;--j}B.a.p(b,"...")
return}}q=A.m(p)
r=A.m(o)
k+=r.length+q.length+4}}if(j>b.length+2){k+=5
m="..."}else m=null
for(;;){if(!(k>80&&b.length>3))break
if(0>=b.length)return A.u(b,-1)
k-=b.pop().length+2
if(m==null){k+=5
m="..."}}if(m!=null)B.a.p(b,m)
B.a.p(b,q)
B.a.p(b,r)},
H(a){A.fY(a)},
p:function p(){},
cc:function cc(a){this.a=a},
a8:function a8(){},
a3:function a3(a,b,c,d){var _=this
_.a=a
_.b=b
_.c=c
_.d=d},
bu:function bu(a,b,c,d,e,f){var _=this
_.e=a
_.f=b
_.a=c
_.b=d
_.c=e
_.d=f},
ck:function ck(a,b,c,d,e){var _=this
_.f=a
_.a=b
_.b=c
_.c=d
_.d=e},
by:function by(a){this.a=a},
cI:function cI(a){this.a=a},
am:function am(a){this.a=a},
ch:function ch(a){this.a=a},
cz:function cz(){},
bw:function bw(){},
aA:function aA(a){this.a=a},
da:function da(a){this.a=a},
b:function b(){},
F:function F(){},
f:function f(){},
cV:function cV(){},
aT:function aT(a){this.a=a},
ds:function ds(a){this.a=a},
ii(a,b,c){t.b.a(a)
if(A.L(c)>=1)return a.$1(b)
return a.$0()},
fM(a){return a==null||A.ed(a)||typeof a=="number"||typeof a=="string"||t.G.b(a)||t.bX.b(a)||t.ca.b(a)||t.c.b(a)||t.c0.b(a)||t.t.b(a)||t.bk.b(a)||t.B.b(a)||t.W.b(a)||t.J.b(a)||t.V.b(a)},
je(a){if(A.fM(a))return a
return new A.eo(new A.bO(t.A)).$1(a)},
eX(a,b){var s=new A.i($.h,b.h("i<0>")),r=new A.ab(s,b.h("ab<0>"))
a.then(A.c8(new A.ey(r,b),1),A.c8(new A.ez(r),1))
return s},
eo:function eo(a){this.a=a},
ey:function ey(a,b){this.a=a
this.b=b},
ez:function ez(a){this.a=a},
il(a){var s,r,q=a.i(0,"content")
if(typeof q=="string")return q
if(t.j.b(q)){s=J.eE(q,t.f)
r=s.$ti
return new A.E(new A.U(s,r.h("G(b.E)").a(new A.eb()),r.h("U<b.E>")),r.h("j(b.E)").a(new A.ec()),r.h("E<b.E,j>")).b7(0,"")}s=A.a1(a.i(0,"text"))
return s==null?"":s},
ep(){var s=0,r=A.d0(t.x),q,p,o,n,m,l,k,j,i
var $async$ep=A.d3(function(a,b){if(a===1)return A.cY(b,r)
for(;;)switch(s){case 0:o=$.d6()
n=t.N
m=t.z
l=t.P.a(A.bl(["sessionKey","main","limit",100],n,m))
k=B.e.ba(1000*Date.now(),16)+"-web"
j=new A.i($.h,t.cU)
o.d.B(0,k,new A.ab(j,t.cS))
o.aG(A.bl(["type","req","id",k,"method","chat.history","params",l],n,m))
i=t.g
s=3
return A.aE(j,$async$ep)
case 3:p=i.a(b.i(0,"messages"))
if(p==null)p=[]
o=J.eE(p,t.f)
n=o.$ti
m=n.h("E<b.E,Q>")
l=m.h("U<b.E>")
o=A.hE(new A.U(new A.E(new A.U(o,n.h("G(b.E)").a(new A.eq()),n.h("U<b.E>")),n.h("Q(b.E)").a(new A.er()),m),m.h("G(b.E)").a(new A.es()),l),l.h("b.E"))
q=o
s=1
break
case 1:return A.cZ(q,r)}})
return A.d_($async$ep,r)},
jk(a){var s,r=null,q=t.d6,p=new A.aU(r,r,r,r,q),o=B.e.ba(1000*Date.now(),16)+"-chat",n=$.d6(),m=t.N
n.aG(A.bl(["type","req","id",o,"method","chat.send","params",A.bl(["sessionKey","main","message",a,"idempotencyKey",o+"-idem"],m,m)],m,t.z))
s=A.cM()
n=n.c
s.b=new A.bD(n,A.e(n).h("bD<1>")).bQ(new A.eC(p,s))
return new A.ao(p,q.h("ao<1>"))},
aO:function aO(a,b,c){this.a=a
this.b=b
this.d=c},
Q:function Q(a,b){this.a=a
this.b=b},
eb:function eb(){},
ec:function ec(){},
eq:function eq(){},
er:function er(){},
es:function es(){},
eC:function eC(a,b){this.a=a
this.b=b},
eA:function eA(){},
eB:function eB(){},
db:function db(a,b,c){var _=this
_.a=null
_.b=!1
_.c=a
_.d=b
_.e=c},
dc:function dc(){},
dd:function dd(a,b){this.a=a
this.b=b},
de:function de(a){this.a=a},
df:function df(a){this.a=a},
aW(a,b,c,d,e){var s,r=A.iX(new A.dJ(c),t.m),q=null
if(r==null)r=q
else{if(typeof r=="function")A.b3(A.b5("Attempting to rewrap a JS function.",null))
s=function(f,g){return function(h){return f(g,h,arguments.length)}}(A.ii,r)
s[$.f_()]=r
r=s}r=new A.bK(a,b,r,!1,e.h("bK<0>"))
r.b0()
return r},
iX(a,b){var s=$.h
if(s===B.b)return a
return s.bH(a,b)},
eG:function eG(a,b){this.a=a
this.$ti=b},
bJ:function bJ(a,b,c,d){var _=this
_.a=a
_.b=b
_.c=c
_.$ti=d},
cO:function cO(a,b,c,d){var _=this
_.a=a
_.b=b
_.c=c
_.$ti=d},
bK:function bK(a,b,c,d,e){var _=this
_.a=0
_.b=a
_.c=b
_.d=c
_.e=d
_.$ti=e},
dJ:function dJ(a){this.a=a},
jg(){var s=v.G,r=A.aY(A.q(s.document).getElementById("chat-input"))
if(r==null)r=A.q(r)
$.c3.b=r
r=A.aY(A.q(s.document).getElementById("send-btn"))
if(r==null)r=A.q(r)
$.cX.b=r
r=A.aY(A.q(s.document).getElementById("messages"))
if(r==null)r=A.q(r)
$.c4.b=r
s=A.aY(A.q(s.document).getElementById("status"))
if(s==null)s=A.q(s)
$.X.b=s
s=t.bU
r=s.h("~(1)?")
s=s.c
A.aW($.cX.q(),"click",r.a(new A.et()),!1,s)
A.aW($.c3.q(),"keypress",r.a(new A.eu()),!1,s)
A.d5()},
d5(){var s=0,r=A.d0(t.H),q=1,p=[],o,n,m,l,k,j,i
var $async$d5=A.d3(function(a,b){if(a===1){p.push(b)
s=q}for(;;)switch(s){case 0:$.X.q().textContent="Connecting..."
q=3
s=6
return A.aE($.d6().bJ(),$async$d5)
case 6:$.X.q().textContent="Loading history..."
q=8
s=11
return A.aE(A.ep(),$async$d5)
case 11:o=b
for(l=J.cb(o);l.k();){n=l.gm()
A.eg(n.a,n.b)}q=3
s=10
break
case 8:q=7
j=p.pop()
s=10
break
case 7:s=3
break
case 10:$.X.q().textContent="Connected"
$.X.q().className="status connected"
$.cX.q().disabled=!1
$.c3.q().focus()
q=1
s=5
break
case 3:q=2
i=p.pop()
m=A.I(i)
l=$.X.q()
l.textContent="Connection failed: "+A.m(m)
$.X.q().className="status error"
s=5
break
case 2:s=1
break
case 5:return A.cZ(null,r)
case 1:return A.cY(p.at(-1),r)}})
return A.d_($async$d5,r)},
ca(){var s=0,r=A.d0(t.H),q,p=2,o=[],n=[],m,l,k,j,i,h,g,f,e
var $async$ca=A.d3(function(a,b){if(a===1){o.push(b)
s=p}for(;;)switch(s){case 0:f=B.c.bV(A.C($.c3.q().value))
if(J.aM(f)!==0){i=$.d6()
if(i.b){i=i.a
i=(i==null?null:A.L(i.readyState))===1}else i=!1
i=!i}else i=!0
if(i){s=1
break}$.c3.q().value=""
$.cX.q().disabled=!0
A.eg("user",f)
$.X.q().textContent="Thinking..."
m=A.eg("assistant","")
A.H("[chat] sending: "+A.m(f))
l=""
p=4
i=new A.aD(A.eh(A.jk(f),"stream",t.K),t.a4)
p=7
case 10:s=12
return A.aE(i.k(),$async$ca)
case 12:if(!b){s=11
break}k=i.gm()
A.fY("[chat] chunk: isFinal="+k.b+' text="'+k.a+'" mediaUrls='+A.m(k.d))
if(k.b){m.textContent=k.a
l=k.a}else if(k.a.length!==0)m.textContent=A.m(A.a1(m.textContent))+k.a
h=$.c4.b
if(h===$.c4)A.b3(A.hB(""))
h.scrollTop=A.L(h.scrollHeight)
s=10
break
case 11:n.push(9)
s=8
break
case 7:n=[4]
case 8:p=4
s=13
return A.aE(i.F(),$async$ca)
case 13:s=n.pop()
break
case 9:$.X.q().textContent="Connected"
$.X.q().className="status connected"
if(J.aM(l)!==0)A.d1(l)
p=2
s=6
break
case 4:p=3
e=o.pop()
j=A.I(e)
A.eg("error","Error: "+A.m(j))
i=$.X.q()
i.textContent="Error"
$.X.q().className="status error"
s=6
break
case 3:s=2
break
case 6:$.cX.q().disabled=!1
$.c3.q().focus()
case 1:return A.cZ(q,r)
case 2:return A.cY(o.at(-1),r)}})
return A.d_($async$ca,r)},
d1(a){return A.iN(a)},
iN(a){var s=0,r=A.d0(t.H),q,p=2,o=[],n,m,l,k,j,i,h
var $async$d1=A.d3(function(b,c){if(b===1){o.push(c)
s=p}for(;;)switch(s){case 0:A.H("[tts] requesting TTS for: "+a.length+" chars")
p=4
j=t.N
s=7
return A.aE(A.eX(A.q(A.q(v.G.window).fetch("/tts",{method:"POST",headers:A.q(A.je(A.bl(["Content-Type","application/json"],j,j))),body:B.f.b4(A.bl(["text",a],j,j),null)})),t.m),$async$d1)
case 7:n=c
A.H("[tts] response: "+A.L(n.status))
if(!A.fD(n.ok)){A.H("[tts] failed: "+A.L(n.status)+" "+A.C(n.statusText))
s=1
break}s=8
return A.aE(A.eX(A.q(n.arrayBuffer()),t.q),$async$d1)
case 8:m=c
l=A.hG(m,0,null)
A.H("[tts] got "+J.aM(l)+" bytes")
A.ex(l)
p=2
s=6
break
case 4:p=3
h=o.pop()
k=A.I(h)
A.H("[tts] error: "+A.m(k))
s=6
break
case 3:s=2
break
case 6:case 1:return A.cZ(q,r)
case 2:return A.cY(o.at(-1),r)}})
return A.d_($async$d1,r)},
ex(a){return A.ji(a)},
ji(a){var s=0,r=A.d0(t.H),q=1,p=[],o,n,m,l,k,j,i
var $async$ex=A.d3(function(b,c){if(b===1){p.push(c)
s=q}for(;;)switch(s){case 0:A.H("onAudioReceived: "+a.length+" bytes")
q=3
o=A.q(new v.G.AudioContext())
A.H("AudioContext state: "+A.C(o.state))
n=t.q.a(B.C.gbI(a))
s=6
return A.aE(A.eX(A.q(o.decodeAudioData(n)),t.m),$async$ex)
case 6:m=c
A.H("Decoded audio: "+A.m(A.eO(m.duration))+"s, "+A.m(A.eO(m.sampleRate))+"Hz, "+A.L(m.numberOfChannels)+"ch")
l=A.q(o.createBufferSource())
l.buffer=m
A.aY(l.connect(A.q(o.destination)))
l.start()
A.H("Audio playback started")
q=1
s=5
break
case 3:q=2
i=p.pop()
k=A.I(i)
A.H("Audio playback error: "+A.m(k))
s=5
break
case 2:s=1
break
case 5:return A.cZ(null,r)
case 1:return A.cY(p.at(-1),r)}})
return A.d_($async$ex,r)},
eg(a,b){var s,r,q,p=v.G,o=A.q(A.q(p.document).createElement("div"))
o.className="message "+a
s=A.q(A.q(p.document).createElement("span"))
s.className="label"
if(a==="user")r="You: "
else r=a==="assistant"?"Agent: ":"Error: "
s.textContent=r
q=A.q(A.q(p.document).createElement("span"))
q.className="body"
q.textContent=b
A.q(o.appendChild(s))
A.q(o.appendChild(q))
A.q($.c4.q().appendChild(o))
$.c4.q().scrollTop=A.L($.c4.q().scrollHeight)
return q},
et:function et(){},
eu:function eu(){},
fY(a){if(typeof dartPrint=="function"){dartPrint(a)
return}if(typeof console=="object"&&typeof console.log!="undefined"){console.log(a)
return}if(typeof print=="function"){print(a)
return}throw"Unable to print message: "+String(a)},
hr(){var s,r,q,p=t.N,o=A.hD(B.l,p,p),n=A.aY(v.G.CLAWFACE_CONFIG)
if(n!=null)for(p=B.l.gD(),p=p.gt(p);p.k();){s=p.gm()
r=n[s]
if(r!=null)q=typeof r==="string"
else q=!1
if(q)o.B(0,s,A.C(r))}return o}},B={}
var w=[A,J,B]
var $={}
A.eH.prototype={}
J.cl.prototype={
H(a,b){return a===b},
gA(a){return A.bt(a)},
j(a){return"Instance of '"+A.cB(a)+"'"},
gv(a){return A.aH(A.eP(this))}}
J.cn.prototype={
j(a){return String(a)},
gA(a){return a?519018:218159},
gv(a){return A.aH(t.y)},
$in:1,
$iG:1}
J.be.prototype={
H(a,b){return null==b},
j(a){return"null"},
gA(a){return 0},
$in:1}
J.bh.prototype={$ir:1}
J.ak.prototype={
gA(a){return 0},
j(a){return String(a)}}
J.cA.prototype={}
J.bx.prototype={}
J.aj.prototype={
j(a){var s=a[$.f_()]
if(s==null)return this.be(a)
return"JavaScript function for "+J.ah(s)},
$iav:1}
J.bg.prototype={
gA(a){return 0},
j(a){return String(a)}}
J.bi.prototype={
gA(a){return 0},
j(a){return String(a)}}
J.x.prototype={
a6(a,b){return new A.a4(a,A.aq(a).h("@<1>").l(b).h("a4<1,2>"))},
p(a,b){A.aq(a).c.a(b)
a.$flags&1&&A.eZ(a,29)
a.push(b)},
bG(a,b){var s
A.aq(a).h("b<1>").a(b)
a.$flags&1&&A.eZ(a,"addAll",2)
for(s=b.gt(b);s.k();)a.push(s.gm())},
X(a,b,c){var s=A.aq(a)
return new A.a6(a,s.l(c).h("1(2)").a(b),s.h("@<1>").l(c).h("a6<1,2>"))},
C(a,b){if(!(b<a.length))return A.u(a,b)
return a[b]},
gu(a){return a.length===0},
gJ(a){return a.length!==0},
j(a){return A.fb(a,"[","]")},
gt(a){return new J.at(a,a.length,A.aq(a).h("at<1>"))},
gA(a){return A.bt(a)},
gn(a){return a.length},
i(a,b){if(!(b>=0&&b<a.length))throw A.c(A.ei(a,b))
return a[b]},
B(a,b,c){A.aq(a).c.a(c)
a.$flags&2&&A.eZ(a)
if(!(b>=0&&b<a.length))throw A.c(A.ei(a,b))
a[b]=c},
aF(a,b){return new A.aa(a,b.h("aa<0>"))},
$id:1,
$ib:1,
$ik:1}
J.cm.prototype={
bW(a){var s,r,q
if(!Array.isArray(a))return null
s=a.$flags|0
if((s&4)!==0)r="const, "
else if((s&2)!==0)r="unmodifiable, "
else r=(s&1)!==0?"fixed, ":""
q="Instance of '"+A.cB(a)+"'"
if(r==="")return q
return q+" ("+r+"length: "+a.length+")"}}
J.dj.prototype={}
J.at.prototype={
gm(){var s=this.d
return s==null?this.$ti.c.a(s):s},
k(){var s,r=this,q=r.a,p=q.length
if(r.b!==p){q=A.jl(q)
throw A.c(q)}s=r.c
if(s>=p){r.d=null
return!1}r.d=q[s]
r.c=s+1
return!0},
$iB:1}
J.bf.prototype={
ba(a,b){var s,r,q,p,o
if(b<2||b>36)throw A.c(A.cC(b,2,36,"radix",null))
s=a.toString(b)
r=s.length
q=r-1
if(!(q>=0))return A.u(s,q)
if(s.charCodeAt(q)!==41)return s
p=/^([\da-z]+)(?:\.([\da-z]+))?\(e\+(\d+)\)$/.exec(s)
if(p==null)A.b3(A.fm("Unexpected toString result: "+s))
r=p.length
if(1>=r)return A.u(p,1)
s=p[1]
if(3>=r)return A.u(p,3)
o=+p[3]
r=p[2]
if(r!=null){s+=r
o-=r.length}return s+B.c.bd("0",o)},
j(a){if(a===0&&1/a<0)return"-0.0"
else return""+a},
gA(a){var s,r,q,p,o=a|0
if(a===o)return o&536870911
s=Math.abs(a)
r=Math.log(s)/0.6931471805599453|0
q=Math.pow(2,r)
p=s<1?s/q:q/s
return((p*9007199254740992|0)+(p*3542243181176521|0))*599197+r*1259&536870911},
aY(a,b){var s
if(a>0)s=this.bE(a,b)
else{s=b>31?31:b
s=a>>s>>>0}return s},
bE(a,b){return b>31?0:a>>>b},
gv(a){return A.aH(t.o)},
$io:1,
$iaL:1}
J.bd.prototype={
gv(a){return A.aH(t.S)},
$in:1,
$ia:1}
J.co.prototype={
gv(a){return A.aH(t.i)},
$in:1}
J.aQ.prototype={
P(a,b,c){return a.substring(b,A.hJ(b,c,a.length))},
bV(a){var s,r,q,p=a.trim(),o=p.length
if(o===0)return p
if(0>=o)return A.u(p,0)
if(p.charCodeAt(0)===133){s=J.hz(p,1)
if(s===o)return""}else s=0
r=o-1
if(!(r>=0))return A.u(p,r)
q=p.charCodeAt(r)===133?J.hA(p,r):o
if(s===0&&q===o)return p
return p.substring(s,q)},
bd(a,b){var s,r
if(0>=b)return""
if(b===1||a.length===0)return a
if(b!==b>>>0)throw A.c(B.u)
for(s=a,r="";;){if((b&1)===1)r=s+r
b=b>>>1
if(b===0)break
s+=s}return r},
j(a){return a},
gA(a){var s,r,q
for(s=a.length,r=0,q=0;q<s;++q){r=r+a.charCodeAt(q)&536870911
r=r+((r&524287)<<10)&536870911
r^=r>>6}r=r+((r&67108863)<<3)&536870911
r^=r>>11
return r+((r&16383)<<15)&536870911},
gv(a){return A.aH(t.N)},
gn(a){return a.length},
$in:1,
$ij:1}
A.an.prototype={
gt(a){return new A.b7(J.cb(this.gI()),A.e(this).h("b7<1,2>"))},
gn(a){return J.aM(this.gI())},
gu(a){return J.hg(this.gI())},
gJ(a){return J.f2(this.gI())},
C(a,b){return A.e(this).y[1].a(J.f1(this.gI(),b))},
j(a){return J.ah(this.gI())}}
A.b7.prototype={
k(){return this.a.k()},
gm(){return this.$ti.y[1].a(this.a.gm())},
$iB:1}
A.au.prototype={
gI(){return this.a}}
A.bI.prototype={$id:1}
A.bF.prototype={
i(a,b){return this.$ti.y[1].a(J.he(this.a,b))},
$id:1,
$ik:1}
A.a4.prototype={
a6(a,b){return new A.a4(this.a,this.$ti.h("@<1>").l(b).h("a4<1,2>"))},
gI(){return this.a}}
A.aw.prototype={
j(a){return"LateInitializationError: "+this.a}}
A.ew.prototype={
$0(){return A.f9(null,t.H)},
$S:11}
A.d.prototype={}
A.R.prototype={
gt(a){var s=this
return new A.ay(s,s.gn(s),A.e(s).h("ay<R.E>"))},
gu(a){return this.gn(this)===0},
X(a,b,c){var s=A.e(this)
return new A.a6(this,s.l(c).h("1(R.E)").a(b),s.h("@<R.E>").l(c).h("a6<1,2>"))}}
A.ay.prototype={
gm(){var s=this.d
return s==null?this.$ti.c.a(s):s},
k(){var s,r=this,q=r.a,p=J.d4(q),o=p.gn(q)
if(r.b!==o)throw A.c(A.aP(q))
s=r.c
if(s>=o){r.d=null
return!1}r.d=p.C(q,s);++r.c
return!0},
$iB:1}
A.E.prototype={
gt(a){var s=this.a
return new A.bm(s.gt(s),this.b,A.e(this).h("bm<1,2>"))},
gn(a){var s=this.a
return s.gn(s)},
gu(a){var s=this.a
return s.gu(s)},
C(a,b){var s=this.a
return this.b.$1(s.C(s,b))}}
A.bb.prototype={$id:1}
A.bm.prototype={
k(){var s=this,r=s.b
if(r.k()){s.a=s.c.$1(r.gm())
return!0}s.a=null
return!1},
gm(){var s=this.a
return s==null?this.$ti.y[1].a(s):s},
$iB:1}
A.a6.prototype={
gn(a){return J.aM(this.a)},
C(a,b){return this.b.$1(J.f1(this.a,b))}}
A.U.prototype={
gt(a){return new A.bz(J.cb(this.a),this.b,this.$ti.h("bz<1>"))},
X(a,b,c){var s=this.$ti
return new A.E(this,s.l(c).h("1(2)").a(b),s.h("@<1>").l(c).h("E<1,2>"))}}
A.bz.prototype={
k(){var s,r
for(s=this.a,r=this.b;s.k();)if(r.$1(s.gm()))return!0
return!1},
gm(){return this.a.gm()},
$iB:1}
A.aa.prototype={
gt(a){return new A.bA(J.cb(this.a),this.$ti.h("bA<1>"))}}
A.bA.prototype={
k(){var s,r
for(s=this.a,r=this.$ti.c;s.k();)if(r.b(s.gm()))return!0
return!1},
gm(){return this.$ti.c.a(this.a.gm())},
$iB:1}
A.D.prototype={}
A.c2.prototype={}
A.b9.prototype={
gu(a){return this.gn(this)===0},
j(a){return A.eJ(this)},
$it:1}
A.ba.prototype={
gn(a){return this.b.length},
gaO(){var s=this.$keys
if(s==null){s=Object.keys(this.a)
this.$keys=s}return s},
W(a){if(typeof a!="string")return!1
if("__proto__"===a)return!1
return this.a.hasOwnProperty(a)},
i(a,b){if(!this.W(b))return null
return this.b[this.a[b]]},
G(a,b){var s,r,q,p
this.$ti.h("~(1,2)").a(b)
s=this.gaO()
r=this.b
for(q=s.length,p=0;p<q;++p)b.$2(s[p],r[p])},
gD(){return new A.bP(this.gaO(),this.$ti.h("bP<1>"))}}
A.bP.prototype={
gn(a){return this.a.length},
gu(a){return 0===this.a.length},
gJ(a){return 0!==this.a.length},
gt(a){var s=this.a
return new A.bQ(s,s.length,this.$ti.h("bQ<1>"))}}
A.bQ.prototype={
gm(){var s=this.d
return s==null?this.$ti.c.a(s):s},
k(){var s=this,r=s.c
if(r>=s.b){s.d=null
return!1}s.d=s.a[r]
s.c=r+1
return!0},
$iB:1}
A.bv.prototype={}
A.dw.prototype={
E(a){var s,r,q=this,p=new RegExp(q.a).exec(a)
if(p==null)return null
s=Object.create(null)
r=q.b
if(r!==-1)s.arguments=p[r+1]
r=q.c
if(r!==-1)s.argumentsExpr=p[r+1]
r=q.d
if(r!==-1)s.expr=p[r+1]
r=q.e
if(r!==-1)s.method=p[r+1]
r=q.f
if(r!==-1)s.receiver=p[r+1]
return s}}
A.bs.prototype={
j(a){return"Null check operator used on a null value"}}
A.cp.prototype={
j(a){var s,r=this,q="NoSuchMethodError: method not found: '",p=r.b
if(p==null)return"NoSuchMethodError: "+r.a
s=r.c
if(s==null)return q+p+"' ("+r.a+")"
return q+p+"' on '"+s+"' ("+r.a+")"}}
A.cJ.prototype={
j(a){var s=this.a
return s.length===0?"Error":"Error: "+s}}
A.dt.prototype={
j(a){return"Throw of null ('"+(this.a===null?"null":"undefined")+"' from JavaScript)"}}
A.bc.prototype={}
A.bV.prototype={
j(a){var s,r=this.b
if(r!=null)return r
r=this.a
s=r!==null&&typeof r==="object"?r.stack:null
return this.b=s==null?"":s},
$iT:1}
A.ai.prototype={
j(a){var s=this.constructor,r=s==null?null:s.name
return"Closure '"+A.h_(r==null?"unknown":r)+"'"},
$iav:1,
gbZ(){return this},
$C:"$1",
$R:1,
$D:null}
A.ce.prototype={$C:"$0",$R:0}
A.cf.prototype={$C:"$2",$R:2}
A.cH.prototype={}
A.cF.prototype={
j(a){var s=this.$static_name
if(s==null)return"Closure of unknown static method"
return"Closure '"+A.h_(s)+"'"}}
A.aN.prototype={
H(a,b){if(b==null)return!1
if(this===b)return!0
if(!(b instanceof A.aN))return!1
return this.$_target===b.$_target&&this.a===b.a},
gA(a){return(A.eW(this.a)^A.bt(this.$_target))>>>0},
j(a){return"Closure '"+this.$_name+"' of "+("Instance of '"+A.cB(this.a)+"'")}}
A.cD.prototype={
j(a){return"RuntimeError: "+this.a}}
A.a5.prototype={
gn(a){return this.a},
gu(a){return this.a===0},
gD(){return new A.ax(this,A.e(this).h("ax<1>"))},
W(a){var s=this.b
if(s==null)return!1
return s[a]!=null},
i(a,b){var s,r,q,p,o=null
if(typeof b=="string"){s=this.b
if(s==null)return o
r=s[b]
q=r==null?o:r.b
return q}else if(typeof b=="number"&&(b&0x3fffffff)===b){p=this.c
if(p==null)return o
r=p[b]
q=r==null?o:r.b
return q}else return this.bO(b)},
bO(a){var s,r,q=this.d
if(q==null)return null
s=q[this.b5(a)]
r=this.b6(s,a)
if(r<0)return null
return s[r].b},
B(a,b,c){var s,r,q=this,p=A.e(q)
p.c.a(b)
p.y[1].a(c)
if(typeof b=="string"){s=q.b
q.aH(s==null?q.b=q.am():s,b,c)}else if(typeof b=="number"&&(b&0x3fffffff)===b){r=q.c
q.aH(r==null?q.c=q.am():r,b,c)}else q.bP(b,c)},
bP(a,b){var s,r,q,p,o=this,n=A.e(o)
n.c.a(a)
n.y[1].a(b)
s=o.d
if(s==null)s=o.d=o.am()
r=o.b5(a)
q=s[r]
if(q==null)s[r]=[o.an(a,b)]
else{p=o.b6(q,a)
if(p>=0)q[p].b=b
else q.push(o.an(a,b))}},
bS(a,b){var s=this.bz(this.b,b)
return s},
G(a,b){var s,r,q=this
A.e(q).h("~(1,2)").a(b)
s=q.e
r=q.r
while(s!=null){b.$2(s.a,s.b)
if(r!==q.r)throw A.c(A.aP(q))
s=s.c}},
aH(a,b,c){var s,r=A.e(this)
r.c.a(b)
r.y[1].a(c)
s=a[b]
if(s==null)a[b]=this.an(b,c)
else s.b=c},
bz(a,b){var s
if(a==null)return null
s=a[b]
if(s==null)return null
this.bF(s)
delete a[b]
return s.b},
aP(){this.r=this.r+1&1073741823},
an(a,b){var s=this,r=A.e(s),q=new A.dn(r.c.a(a),r.y[1].a(b))
if(s.e==null)s.e=s.f=q
else{r=s.f
r.toString
q.d=r
s.f=r.c=q}++s.a
s.aP()
return q},
bF(a){var s=this,r=a.d,q=a.c
if(r==null)s.e=q
else r.c=q
if(q==null)s.f=r
else q.d=r;--s.a
s.aP()},
b5(a){return J.eD(a)&1073741823},
b6(a,b){var s,r
if(a==null)return-1
s=a.length
for(r=0;r<s;++r)if(J.P(a[r].a,b))return r
return-1},
j(a){return A.eJ(this)},
am(){var s=Object.create(null)
s["<non-identifier-key>"]=s
delete s["<non-identifier-key>"]
return s},
$ife:1}
A.dn.prototype={}
A.ax.prototype={
gn(a){return this.a.a},
gu(a){return this.a.a===0},
gt(a){var s=this.a
return new A.bk(s,s.r,s.e,this.$ti.h("bk<1>"))}}
A.bk.prototype={
gm(){return this.d},
k(){var s,r=this,q=r.a
if(r.b!==q.r)throw A.c(A.aP(q))
s=r.c
if(s==null){r.d=null
return!1}else{r.d=s.a
r.c=s.c
return!0}},
$iB:1}
A.ek.prototype={
$1(a){return this.a(a)},
$S:6}
A.el.prototype={
$2(a,b){return this.a(a,b)},
$S:12}
A.em.prototype={
$1(a){return this.a(A.C(a))},
$S:13}
A.dI.prototype={
aU(){var s=this.b
if(s===this)throw A.c(new A.aw("Local '' has not been initialized."))
return s},
q(){var s=this.b
if(s===this)throw A.c(new A.aw("Field '' has not been initialized."))
return s}}
A.al.prototype={
gv(a){return B.E},
$in:1,
$ial:1,
$ib6:1}
A.aR.prototype={$iaR:1}
A.bp.prototype={
gbI(a){if(((a.$flags|0)&2)!==0)return new A.cW(a.buffer)
else return a.buffer}}
A.cW.prototype={$ib6:1}
A.cr.prototype={
gv(a){return B.F},
$in:1,
$ieF:1}
A.aS.prototype={
gn(a){return a.length},
$iJ:1}
A.bn.prototype={
i(a,b){A.aF(b,a,a.length)
return a[b]},
$id:1,
$ib:1,
$ik:1}
A.bo.prototype={$id:1,$ib:1,$ik:1}
A.cs.prototype={
gv(a){return B.G},
$in:1,
$id8:1}
A.ct.prototype={
gv(a){return B.H},
$in:1,
$id9:1}
A.cu.prototype={
gv(a){return B.I},
i(a,b){A.aF(b,a,a.length)
return a[b]},
$in:1,
$idg:1}
A.cv.prototype={
gv(a){return B.J},
i(a,b){A.aF(b,a,a.length)
return a[b]},
$in:1,
$idh:1}
A.cw.prototype={
gv(a){return B.K},
i(a,b){A.aF(b,a,a.length)
return a[b]},
$in:1,
$idi:1}
A.cx.prototype={
gv(a){return B.L},
i(a,b){A.aF(b,a,a.length)
return a[b]},
$in:1,
$idy:1}
A.cy.prototype={
gv(a){return B.M},
i(a,b){A.aF(b,a,a.length)
return a[b]},
$in:1,
$idz:1}
A.bq.prototype={
gv(a){return B.N},
gn(a){return a.length},
i(a,b){A.aF(b,a,a.length)
return a[b]},
$in:1,
$idA:1}
A.br.prototype={
gv(a){return B.O},
gn(a){return a.length},
i(a,b){A.aF(b,a,a.length)
return a[b]},
$in:1,
$idB:1}
A.bR.prototype={}
A.bS.prototype={}
A.bT.prototype={}
A.bU.prototype={}
A.S.prototype={
h(a){return A.e6(v.typeUniverse,this,a)},
l(a){return A.i8(v.typeUniverse,this,a)}}
A.cQ.prototype={}
A.e4.prototype={
j(a){return A.M(this.a,null)}}
A.cP.prototype={
j(a){return this.a}}
A.bY.prototype={$ia8:1}
A.dD.prototype={
$1(a){var s=this.a,r=s.a
s.a=null
r.$0()},
$S:7}
A.dC.prototype={
$1(a){var s,r
this.a.a=t.M.a(a)
s=this.b
r=this.c
s.firstChild?s.removeChild(r):s.appendChild(r)},
$S:14}
A.dE.prototype={
$0(){this.a.$0()},
$S:8}
A.dF.prototype={
$0(){this.a.$0()},
$S:8}
A.e2.prototype={
bf(a,b){if(self.setTimeout!=null)self.setTimeout(A.c8(new A.e3(this,b),0),a)
else throw A.c(A.fm("`setTimeout()` not found."))}}
A.e3.prototype={
$0(){this.b.$0()},
$S:0}
A.bB.prototype={
V(a){var s,r=this,q=r.$ti
q.h("1/?").a(a)
if(a==null)a=q.c.a(a)
if(!r.b)r.a.K(a)
else{s=r.a
if(q.h("Z<1>").b(a))s.aJ(a)
else s.ag(a)}},
a7(a,b){var s
if(b==null)b=A.d7(a)
s=this.a
if(this.b)s.S(new A.A(a,b))
else s.R(new A.A(a,b))},
N(a){return this.a7(a,null)},
$ib8:1}
A.e8.prototype={
$1(a){return this.a.$2(0,a)},
$S:2}
A.e9.prototype={
$2(a,b){this.a.$2(1,new A.bc(a,t.l.a(b)))},
$S:15}
A.ef.prototype={
$2(a,b){this.a(A.L(a),b)},
$S:16}
A.A.prototype={
j(a){return A.m(this.a)},
$ip:1,
gO(){return this.b}}
A.bD.prototype={}
A.a_.prototype={
L(){},
M(){},
sa4(a){this.ch=this.$ti.h("a_<1>?").a(a)},
saq(a){this.CW=this.$ti.h("a_<1>?").a(a)}}
A.bE.prototype={
gbp(){return this.c<4},
bA(a){var s,r
A.e(this).h("a_<1>").a(a)
s=a.CW
r=a.ch
if(s==null)this.d=r
else s.sa4(r)
if(r==null)this.e=s
else r.saq(s)
a.saq(a)
a.sa4(a)},
aZ(a,b,c,d){var s,r,q,p,o,n,m,l=this,k=A.e(l)
k.h("~(1)?").a(a)
t.Z.a(c)
if((l.c&4)!==0){k=new A.aV($.h,k.h("aV<1>"))
A.eY(k.gaR())
if(c!=null)k.c=t.M.a(c)
return k}s=$.h
r=d?1:0
q=b!=null?32:0
t.p.l(k.c).h("1(2)").a(a)
p=A.fo(s,b)
o=c==null?A.fT():c
k=k.h("a_<1>")
n=new A.a_(l,a,p,t.M.a(o),s,r|q,k)
n.CW=n
n.ch=n
k.a(n)
n.ay=l.c&1
m=l.e
l.e=n
n.sa4(null)
n.saq(m)
if(m==null)l.d=n
else m.sa4(n)
if(l.d==l.e)A.d2(l.a)
return n},
aV(a){var s=this,r=A.e(s)
a=r.h("a_<1>").a(r.h("K<1>").a(a))
if(a.ch===a)return null
r=a.ay
if((r&2)!==0)a.ay=r|4
else{s.bA(a)
if((s.c&2)===0&&s.d==null)s.bh()}return null},
aW(a){A.e(this).h("K<1>").a(a)},
aX(a){A.e(this).h("K<1>").a(a)},
bg(){if((this.c&4)!==0)return new A.am("Cannot add new events after calling close")
return new A.am("Cannot add new events while doing an addStream")},
bh(){if((this.c&4)!==0){var s=this.r
if((s.a&30)===0)s.K(null)}A.d2(this.b)},
$icG:1,
$icU:1,
$iV:1}
A.bC.prototype={
U(a){var s,r=this.$ti
r.c.a(a)
for(s=this.d,r=r.h("ad<1>");s!=null;s=s.ch)s.a1(new A.ad(a,r))}}
A.bG.prototype={
a7(a,b){var s=this.a
if((s.a&30)!==0)throw A.c(A.cE("Future already completed"))
s.R(A.fH(a,b))},
N(a){return this.a7(a,null)},
$ib8:1}
A.ab.prototype={
V(a){var s,r=this.$ti
r.h("1/?").a(a)
s=this.a
if((s.a&30)!==0)throw A.c(A.cE("Future already completed"))
s.K(r.h("1/").a(a))}}
A.af.prototype={
bR(a){if((this.c&15)!==6)return!0
return this.b.b.aD(t.bG.a(this.d),a.a,t.y,t.K)},
bN(a){var s,r=this,q=r.e,p=null,o=t.z,n=t.K,m=a.a,l=r.b.b
if(t.Q.b(q))p=l.bT(q,m,a.b,o,n,t.l)
else p=l.aD(t.v.a(q),m,o,n)
try{o=r.$ti.h("2/").a(p)
return o}catch(s){if(t.b7.b(A.I(s))){if((r.c&1)!==0)throw A.c(A.b5("The error handler of Future.then must return a value of the returned future's type","onError"))
throw A.c(A.b5("The error handler of Future.catchError must return a value of the future's type","onError"))}else throw s}}}
A.i.prototype={
b9(a,b,c){var s,r,q=this.$ti
q.l(c).h("1/(2)").a(a)
s=$.h
if(s===B.b){if(!t.Q.b(b)&&!t.v.b(b))throw A.c(A.f3(b,"onError",u.c))}else{c.h("@<0/>").l(q.c).h("1(2)").a(a)
b=A.iM(b,s)}r=new A.i(s,c.h("i<0>"))
this.a0(new A.af(r,3,a,b,q.h("@<1>").l(c).h("af<1,2>")))
return r},
b_(a,b,c){var s,r=this.$ti
r.l(c).h("1/(2)").a(a)
s=new A.i($.h,c.h("i<0>"))
this.a0(new A.af(s,19,a,b,r.h("@<1>").l(c).h("af<1,2>")))
return s},
aa(a){var s,r
t.O.a(a)
s=this.$ti
r=new A.i($.h,s)
this.a0(new A.af(r,8,a,null,s.h("af<1,1>")))
return r},
bD(a){this.$ti.c.a(a)
this.a=8
this.c=a},
bB(a){this.a=this.a&1|16
this.c=a},
a2(a){this.a=a.a&30|this.a&1
this.c=a.c},
a0(a){var s,r=this,q=r.a
if(q<=3){a.a=t.F.a(r.c)
r.c=a}else{if((q&4)!==0){s=t._.a(r.c)
if((s.a&24)===0){s.a0(a)
return}r.a2(s)}A.b_(null,null,r.b,t.M.a(new A.dK(r,a)))}},
aT(a){var s,r,q,p,o,n,m=this,l={}
l.a=a
if(a==null)return
s=m.a
if(s<=3){r=t.F.a(m.c)
m.c=a
if(r!=null){q=a.a
for(p=a;q!=null;p=q,q=o)o=q.a
p.a=r}}else{if((s&4)!==0){n=t._.a(m.c)
if((n.a&24)===0){n.aT(a)
return}m.a2(n)}l.a=m.a5(a)
A.b_(null,null,m.b,t.M.a(new A.dO(l,m)))}},
T(){var s=t.F.a(this.c)
this.c=null
return this.a5(s)},
a5(a){var s,r,q
for(s=a,r=null;s!=null;r=s,s=q){q=s.a
s.a=r}return r},
aL(a){var s,r=this,q=r.$ti
q.h("1/").a(a)
s=r.T()
q.c.a(a)
r.a=8
r.c=a
A.aB(r,s)},
ag(a){var s,r=this
r.$ti.c.a(a)
s=r.T()
r.a=8
r.c=a
A.aB(r,s)},
bk(a){var s,r,q=this
if((a.a&16)!==0){s=q.b===a.b
s=!(s||s)}else s=!1
if(s)return
r=q.T()
q.a2(a)
A.aB(q,r)},
S(a){var s=this.T()
this.bB(a)
A.aB(this,s)},
bj(a,b){A.a0(a)
t.l.a(b)
this.S(new A.A(a,b))},
K(a){var s=this.$ti
s.h("1/").a(a)
if(s.h("Z<1>").b(a)){this.aJ(a)
return}this.aI(a)},
aI(a){var s=this
s.$ti.c.a(a)
s.a^=2
A.b_(null,null,s.b,t.M.a(new A.dM(s,a)))},
aJ(a){A.eL(this.$ti.h("Z<1>").a(a),this,!1)
return},
R(a){this.a^=2
A.b_(null,null,this.b,t.M.a(new A.dL(this,a)))},
$iZ:1}
A.dK.prototype={
$0(){A.aB(this.a,this.b)},
$S:0}
A.dO.prototype={
$0(){A.aB(this.b,this.a.a)},
$S:0}
A.dN.prototype={
$0(){A.eL(this.a.a,this.b,!0)},
$S:0}
A.dM.prototype={
$0(){this.a.ag(this.b)},
$S:0}
A.dL.prototype={
$0(){this.a.S(this.b)},
$S:0}
A.dR.prototype={
$0(){var s,r,q,p,o,n,m,l,k=this,j=null
try{q=k.a.a
j=q.b.b.b8(t.O.a(q.d),t.z)}catch(p){s=A.I(p)
r=A.ag(p)
if(k.c&&t.n.a(k.b.a.c).a===s){q=k.a
q.c=t.n.a(k.b.a.c)}else{q=s
o=r
if(o==null)o=A.d7(q)
n=k.a
n.c=new A.A(q,o)
q=n}q.b=!0
return}if(j instanceof A.i&&(j.a&24)!==0){if((j.a&16)!==0){q=k.a
q.c=t.n.a(j.c)
q.b=!0}return}if(j instanceof A.i){m=k.b.a
l=new A.i(m.b,m.$ti)
j.b9(new A.dS(l,m),new A.dT(l),t.H)
q=k.a
q.c=l
q.b=!1}},
$S:0}
A.dS.prototype={
$1(a){this.a.bk(this.b)},
$S:7}
A.dT.prototype={
$2(a,b){A.a0(a)
t.l.a(b)
this.a.S(new A.A(a,b))},
$S:17}
A.dQ.prototype={
$0(){var s,r,q,p,o,n,m,l
try{q=this.a
p=q.a
o=p.$ti
n=o.c
m=n.a(this.b)
q.c=p.b.b.aD(o.h("2/(1)").a(p.d),m,o.h("2/"),n)}catch(l){s=A.I(l)
r=A.ag(l)
q=s
p=r
if(p==null)p=A.d7(q)
o=this.a
o.c=new A.A(q,p)
o.b=!0}},
$S:0}
A.dP.prototype={
$0(){var s,r,q,p,o,n,m,l=this
try{s=t.n.a(l.a.a.c)
p=l.b
if(p.a.bR(s)&&p.a.e!=null){p.c=p.a.bN(s)
p.b=!1}}catch(o){r=A.I(o)
q=A.ag(o)
p=t.n.a(l.a.a.c)
if(p.a===r){n=l.b
n.c=p
p=n}else{p=r
n=q
if(n==null)n=A.d7(p)
m=l.b
m.c=new A.A(p,n)
p=m}p.b=!0}},
$S:0}
A.cK.prototype={}
A.a7.prototype={
gn(a){var s={},r=new A.i($.h,t.aQ)
s.a=0
this.a8(new A.du(s,this),!0,new A.dv(s,r),r.gbi())
return r}}
A.du.prototype={
$1(a){A.e(this.b).c.a(a);++this.a.a},
$S(){return A.e(this.b).h("~(1)")}}
A.dv.prototype={
$0(){this.b.aL(this.a.a)},
$S:0}
A.bW.prototype={
gbx(){var s,r=this
if((r.b&8)===0)return A.e(r).h("W<1>?").a(r.a)
s=A.e(r)
return s.h("W<1>?").a(s.h("bX<1>").a(r.a).gaw())},
ah(){var s,r,q=this
if((q.b&8)===0){s=q.a
if(s==null)s=q.a=new A.W(A.e(q).h("W<1>"))
return A.e(q).h("W<1>").a(s)}r=A.e(q)
s=r.h("bX<1>").a(q.a).gaw()
return r.h("W<1>").a(s)},
gav(){var s=this.a
if((this.b&8)!==0)s=t.cN.a(s).gaw()
return A.e(this).h("ac<1>").a(s)},
ac(){if((this.b&4)!==0)return new A.am("Cannot add event after closing")
return new A.am("Cannot add event while adding a stream")},
aM(){var s=this.c
if(s==null)s=this.c=(this.b&2)!==0?$.b4():new A.i($.h,t.D)
return s},
p(a,b){var s,r=this,q=A.e(r)
q.c.a(b)
s=r.b
if(s>=4)throw A.c(r.ac())
if((s&1)!==0)r.U(b)
else if((s&3)===0)r.ah().p(0,new A.ad(b,q.h("ad<1>")))},
b3(){var s=this,r=s.b
if((r&4)!==0)return s.aM()
if(r>=4)throw A.c(s.ac())
r=s.b=r|4
if((r&1)!==0)s.ar()
else if((r&3)===0)s.ah().p(0,B.k)
return s.aM()},
aZ(a,b,c,d){var s,r,q,p=this,o=A.e(p)
o.h("~(1)?").a(a)
t.Z.a(c)
if((p.b&3)!==0)throw A.c(A.cE("Stream has already been listened to."))
s=A.hR(p,a,b,c,d,o.c)
r=p.gbx()
if(((p.b|=1)&8)!==0){q=o.h("bX<1>").a(p.a)
q.saw(s)
q.Z()}else p.a=s
s.bC(r)
s.al(new A.e1(p))
return s},
aV(a){var s,r,q,p,o,n,m,l,k=this,j=A.e(k)
j.h("K<1>").a(a)
s=null
if((k.b&8)!==0)s=j.h("bX<1>").a(k.a).F()
k.a=null
k.b=k.b&4294967286|2
r=k.r
if(r!=null)if(s==null)try{q=r.$0()
if(q instanceof A.i)s=q}catch(n){p=A.I(n)
o=A.ag(n)
m=new A.i($.h,t.D)
j=A.a0(p)
l=t.l.a(o)
m.R(new A.A(j,l))
s=m}else s=s.aa(r)
j=new A.e0(k)
if(s!=null)s=s.aa(j)
else j.$0()
return s},
aW(a){var s=this,r=A.e(s)
r.h("K<1>").a(a)
if((s.b&8)!==0)r.h("bX<1>").a(s.a).a9()
A.d2(s.e)},
aX(a){var s=this,r=A.e(s)
r.h("K<1>").a(a)
if((s.b&8)!==0)r.h("bX<1>").a(s.a).Z()
A.d2(s.f)},
$icG:1,
$icU:1,
$iV:1}
A.e1.prototype={
$0(){A.d2(this.a.d)},
$S:0}
A.e0.prototype={
$0(){var s=this.a.c
if(s!=null&&(s.a&30)===0)s.K(null)},
$S:0}
A.cL.prototype={
U(a){var s=this.$ti
s.c.a(a)
this.gav().a1(new A.ad(a,s.h("ad<1>")))},
au(a,b){this.gav().a1(new A.bH(a,b))},
ar(){this.gav().a1(B.k)}}
A.aU.prototype={}
A.ao.prototype={
gA(a){return(A.bt(this.a)^892482866)>>>0},
H(a,b){if(b==null)return!1
if(this===b)return!0
return b instanceof A.ao&&b.a===this.a}}
A.ac.prototype={
aQ(){return this.w.aV(this)},
L(){this.w.aW(this)},
M(){this.w.aX(this)}}
A.az.prototype={
bC(a){var s=this
A.e(s).h("W<1>?").a(a)
if(a==null)return
s.r=a
if(a.c!=null){s.e=(s.e|128)>>>0
a.a_(s)}},
a9(){var s,r,q=this,p=q.e
if((p&8)!==0)return
s=(p+256|4)>>>0
q.e=s
if(p<256){r=q.r
if(r!=null)if(r.a===1)r.a=3}if((p&4)===0&&(s&64)===0)q.al(q.gao())},
Z(){var s=this,r=s.e
if((r&8)!==0)return
if(r>=256){r=s.e=r-256
if(r<256)if((r&128)!==0&&s.r.c!=null)s.r.a_(s)
else{r=(r&4294967291)>>>0
s.e=r
if((r&64)===0)s.al(s.gap())}}},
F(){var s=this,r=(s.e&4294967279)>>>0
s.e=r
if((r&8)===0)s.ad()
r=s.f
return r==null?$.b4():r},
ad(){var s,r=this,q=r.e=(r.e|8)>>>0
if((q&128)!==0){s=r.r
if(s.a===1)s.a=3}if((q&64)===0)r.r=null
r.f=r.aQ()},
L(){},
M(){},
aQ(){return null},
a1(a){var s,r=this,q=r.r
if(q==null)q=r.r=new A.W(A.e(r).h("W<1>"))
q.p(0,a)
s=r.e
if((s&128)===0){s=(s|128)>>>0
r.e=s
if(s<256)q.a_(r)}},
U(a){var s,r=this,q=A.e(r).c
q.a(a)
s=r.e
r.e=(s|64)>>>0
r.d.aE(r.a,a,q)
r.e=(r.e&4294967231)>>>0
r.af((s&4)!==0)},
au(a,b){var s,r=this,q=r.e,p=new A.dH(r,a,b)
if((q&1)!==0){r.e=(q|16)>>>0
r.ad()
s=r.f
if(s!=null&&s!==$.b4())s.aa(p)
else p.$0()}else{p.$0()
r.af((q&4)!==0)}},
ar(){var s,r=this,q=new A.dG(r)
r.ad()
r.e=(r.e|16)>>>0
s=r.f
if(s!=null&&s!==$.b4())s.aa(q)
else q.$0()},
al(a){var s,r=this
t.M.a(a)
s=r.e
r.e=(s|64)>>>0
a.$0()
r.e=(r.e&4294967231)>>>0
r.af((s&4)!==0)},
af(a){var s,r,q=this,p=q.e
if((p&128)!==0&&q.r.c==null){p=q.e=(p&4294967167)>>>0
s=!1
if((p&4)!==0)if(p<256){s=q.r
s=s==null?null:s.c==null
s=s!==!1}if(s){p=(p&4294967291)>>>0
q.e=p}}for(;;a=r){if((p&8)!==0){q.r=null
return}r=(p&4)!==0
if(a===r)break
q.e=(p^64)>>>0
if(r)q.L()
else q.M()
p=(q.e&4294967231)>>>0
q.e=p}if((p&128)!==0&&p<256)q.r.a_(q)},
$iK:1,
$iV:1}
A.dH.prototype={
$0(){var s,r,q,p=this.a,o=p.e
if((o&8)!==0&&(o&16)===0)return
p.e=(o|64)>>>0
s=p.b
o=this.b
r=t.K
q=p.d
if(t.e.b(s))q.bU(s,o,this.c,r,t.l)
else q.aE(t.u.a(s),o,r)
p.e=(p.e&4294967231)>>>0},
$S:0}
A.dG.prototype={
$0(){var s=this.a,r=s.e
if((r&16)===0)return
s.e=(r|74)>>>0
s.d.aC(s.c)
s.e=(s.e&4294967231)>>>0},
$S:0}
A.aX.prototype={
a8(a,b,c,d){var s=A.e(this)
s.h("~(1)?").a(a)
t.Z.a(c)
return this.a.aZ(s.h("~(1)?").a(a),d,c,b===!0)},
bQ(a){return this.a8(a,null,null,null)}}
A.ae.prototype={
sY(a){this.a=t.cd.a(a)},
gY(){return this.a}}
A.ad.prototype={
aA(a){this.$ti.h("V<1>").a(a).U(this.b)}}
A.bH.prototype={
aA(a){a.au(this.b,this.c)}}
A.cN.prototype={
aA(a){a.ar()},
gY(){return null},
sY(a){throw A.c(A.cE("No events after a done."))},
$iae:1}
A.W.prototype={
a_(a){var s,r=this
r.$ti.h("V<1>").a(a)
s=r.a
if(s===1)return
if(s>=1){r.a=1
return}A.eY(new A.dY(r,a))
r.a=1},
p(a,b){var s=this,r=s.c
if(r==null)s.b=s.c=b
else{r.sY(b)
s.c=b}}}
A.dY.prototype={
$0(){var s,r,q,p=this.a,o=p.a
p.a=0
if(o===3)return
s=p.$ti.h("V<1>").a(this.b)
r=p.b
q=r.gY()
p.b=q
if(q==null)p.c=null
r.aA(s)},
$S:0}
A.aV.prototype={
a9(){var s=this.a
if(s>=0)this.a=s+2},
Z(){var s=this,r=s.a-2
if(r<0)return
if(r===0){s.a=1
A.eY(s.gaR())}else s.a=r},
F(){this.a=-1
this.c=null
return $.b4()},
bw(){var s,r=this,q=r.a-1
if(q===0){r.a=-1
s=r.c
if(s!=null){r.c=null
r.b.aC(s)}}else r.a=q},
$iK:1}
A.aD.prototype={
gm(){var s=this
if(s.c)return s.$ti.c.a(s.b)
return s.$ti.c.a(null)},
k(){var s,r=this,q=r.a
if(q!=null){if(r.c){s=new A.i($.h,t.k)
r.b=s
r.c=!1
q.Z()
return s}throw A.c(A.cE("Already waiting for next."))}return r.bo()},
bo(){var s,r,q=this,p=q.b
if(p!=null){q.$ti.h("a7<1>").a(p)
s=new A.i($.h,t.k)
q.b=s
r=p.a8(q.gbq(),!0,q.gbs(),q.gbu())
if(q.b!=null)q.a=r
return s}return $.h1()},
F(){var s=this,r=s.a,q=s.b
s.b=null
if(r!=null){s.a=null
if(!s.c)t.k.a(q).K(!1)
else s.c=!1
return r.F()}return $.b4()},
br(a){var s,r,q=this
q.$ti.c.a(a)
if(q.a==null)return
s=t.k.a(q.b)
q.b=a
q.c=!0
s.aL(!0)
if(q.c){r=q.a
if(r!=null)r.a9()}},
bv(a,b){var s,r,q=this
A.a0(a)
t.l.a(b)
s=q.a
r=t.k.a(q.b)
q.b=q.a=null
if(s!=null)r.S(new A.A(a,b))
else r.R(new A.A(a,b))},
bt(){var s=this,r=s.a,q=t.k.a(s.b)
s.b=s.a=null
if(r!=null)q.ag(!1)
else q.aI(!1)}}
A.c1.prototype={$ifn:1}
A.cT.prototype={
aC(a){var s,r,q
t.M.a(a)
try{if(B.b===$.h){a.$0()
return}A.fN(null,null,this,a,t.H)}catch(q){s=A.I(q)
r=A.ag(q)
A.c7(A.a0(s),t.l.a(r))}},
aE(a,b,c){var s,r,q
c.h("~(0)").a(a)
c.a(b)
try{if(B.b===$.h){a.$1(b)
return}A.fP(null,null,this,a,b,t.H,c)}catch(q){s=A.I(q)
r=A.ag(q)
A.c7(A.a0(s),t.l.a(r))}},
bU(a,b,c,d,e){var s,r,q
d.h("@<0>").l(e).h("~(1,2)").a(a)
d.a(b)
e.a(c)
try{if(B.b===$.h){a.$2(b,c)
return}A.fO(null,null,this,a,b,c,t.H,d,e)}catch(q){s=A.I(q)
r=A.ag(q)
A.c7(A.a0(s),t.l.a(r))}},
b2(a){return new A.dZ(this,t.M.a(a))},
bH(a,b){return new A.e_(this,b.h("~(0)").a(a),b)},
b8(a,b){b.h("0()").a(a)
if($.h===B.b)return a.$0()
return A.fN(null,null,this,a,b)},
aD(a,b,c,d){c.h("@<0>").l(d).h("1(2)").a(a)
d.a(b)
if($.h===B.b)return a.$1(b)
return A.fP(null,null,this,a,b,c,d)},
bT(a,b,c,d,e,f){d.h("@<0>").l(e).l(f).h("1(2,3)").a(a)
e.a(b)
f.a(c)
if($.h===B.b)return a.$2(b,c)
return A.fO(null,null,this,a,b,c,d,e,f)},
aB(a,b,c,d){return b.h("@<0>").l(c).l(d).h("1(2,3)").a(a)}}
A.dZ.prototype={
$0(){return this.a.aC(this.b)},
$S:0}
A.e_.prototype={
$1(a){var s=this.c
return this.a.aE(this.b,s.a(a),s)},
$S(){return this.c.h("~(0)")}}
A.ee.prototype={
$0(){A.ht(this.a,this.b)},
$S:0}
A.bL.prototype={
gn(a){return this.a},
gu(a){return this.a===0},
gD(){return new A.bM(this,this.$ti.h("bM<1>"))},
W(a){var s,r
if(typeof a=="string"&&a!=="__proto__"){s=this.b
return s==null?!1:s[a]!=null}else if(typeof a=="number"&&(a&1073741823)===a){r=this.c
return r==null?!1:r[a]!=null}else return this.bl(a)},
bl(a){var s=this.d
if(s==null)return!1
return this.ak(this.aN(s,a),a)>=0},
i(a,b){var s,r,q
if(typeof b=="string"&&b!=="__proto__"){s=this.b
r=s==null?null:A.fq(s,b)
return r}else if(typeof b=="number"&&(b&1073741823)===b){q=this.c
r=q==null?null:A.fq(q,b)
return r}else return this.bm(b)},
bm(a){var s,r,q=this.d
if(q==null)return null
s=this.aN(q,a)
r=this.ak(s,a)
return r<0?null:s[r+1]},
B(a,b,c){var s,r,q,p,o=this,n=o.$ti
n.c.a(b)
n.y[1].a(c)
s=o.d
if(s==null)s=o.d=A.hS()
r=A.eW(b)&1073741823
q=s[r]
if(q==null){A.fr(s,r,[b,c]);++o.a
o.e=null}else{p=o.ak(q,b)
if(p>=0)q[p+1]=c
else{q.push(b,c);++o.a
o.e=null}}},
G(a,b){var s,r,q,p,o,n,m=this,l=m.$ti
l.h("~(1,2)").a(b)
s=m.aK()
for(r=s.length,q=l.c,l=l.y[1],p=0;p<r;++p){o=s[p]
q.a(o)
n=m.i(0,o)
b.$2(o,n==null?l.a(n):n)
if(s!==m.e)throw A.c(A.aP(m))}},
aK(){var s,r,q,p,o,n,m,l,k,j,i=this,h=i.e
if(h!=null)return h
h=A.ff(i.a,null,!1,t.z)
s=i.b
r=0
if(s!=null){q=Object.getOwnPropertyNames(s)
p=q.length
for(o=0;o<p;++o){h[r]=q[o];++r}}n=i.c
if(n!=null){q=Object.getOwnPropertyNames(n)
p=q.length
for(o=0;o<p;++o){h[r]=+q[o];++r}}m=i.d
if(m!=null){q=Object.getOwnPropertyNames(m)
p=q.length
for(o=0;o<p;++o){l=m[q[o]]
k=l.length
for(j=0;j<k;j+=2){h[r]=l[j];++r}}}return i.e=h},
aN(a,b){return a[A.eW(b)&1073741823]}}
A.bO.prototype={
ak(a,b){var s,r,q
if(a==null)return-1
s=a.length
for(r=0;r<s;r+=2){q=a[r]
if(q==null?b==null:q===b)return r}return-1}}
A.bM.prototype={
gn(a){return this.a.a},
gu(a){return this.a.a===0},
gJ(a){return this.a.a!==0},
gt(a){var s=this.a
return new A.bN(s,s.aK(),this.$ti.h("bN<1>"))}}
A.bN.prototype={
gm(){var s=this.d
return s==null?this.$ti.c.a(s):s},
k(){var s=this,r=s.b,q=s.c,p=s.a
if(r!==p.e)throw A.c(A.aP(p))
else if(q>=r.length){s.d=null
return!1}else{s.d=r[q]
s.c=q+1
return!0}},
$iB:1}
A.dq.prototype={
$2(a,b){this.a.B(0,this.b.a(a),this.c.a(b))},
$S:19}
A.l.prototype={
gt(a){return new A.ay(a,this.gn(a),A.aJ(a).h("ay<l.E>"))},
C(a,b){return this.i(a,b)},
gu(a){return this.gn(a)===0},
gJ(a){return!this.gu(a)},
aF(a,b){return new A.aa(a,b.h("aa<0>"))},
X(a,b,c){var s=A.aJ(a)
return new A.a6(a,s.l(c).h("1(l.E)").a(b),s.h("@<l.E>").l(c).h("a6<1,2>"))},
a6(a,b){return new A.a4(a,A.aJ(a).h("@<l.E>").l(b).h("a4<1,2>"))},
j(a){return A.fb(a,"[","]")}}
A.y.prototype={
G(a,b){var s,r,q,p=A.e(this)
p.h("~(y.K,y.V)").a(b)
for(s=this.gD(),s=s.gt(s),p=p.h("y.V");s.k();){r=s.gm()
q=this.i(0,r)
b.$2(r,q==null?p.a(q):q)}},
gn(a){var s=this.gD()
return s.gn(s)},
gu(a){var s=this.gD()
return s.gu(s)},
j(a){return A.eJ(this)},
$it:1}
A.dr.prototype={
$2(a,b){var s,r=this.a
if(!r.a)this.b.a+=", "
r.a=!1
r=this.b
s=A.m(a)
r.a=(r.a+=s)+": "
s=A.m(b)
r.a+=s},
$S:9}
A.cR.prototype={
i(a,b){var s,r=this.b
if(r==null)return this.c.i(0,b)
else if(typeof b!="string")return null
else{s=r[b]
return typeof s=="undefined"?this.by(b):s}},
gn(a){return this.b==null?this.c.a:this.a3().length},
gu(a){return this.gn(0)===0},
gD(){if(this.b==null){var s=this.c
return new A.ax(s,A.e(s).h("ax<1>"))}return new A.cS(this)},
G(a,b){var s,r,q,p,o=this
t.cQ.a(b)
if(o.b==null)return o.c.G(0,b)
s=o.a3()
for(r=0;r<s.length;++r){q=s[r]
p=o.b[q]
if(typeof p=="undefined"){p=A.ea(o.a[q])
o.b[q]=p}b.$2(q,p)
if(s!==o.c)throw A.c(A.aP(o))}},
a3(){var s=t.g.a(this.c)
if(s==null)s=this.c=A.Y(Object.keys(this.a),t.s)
return s},
by(a){var s
if(!Object.prototype.hasOwnProperty.call(this.a,a))return null
s=A.ea(this.a[a])
return this.b[a]=s}}
A.cS.prototype={
gn(a){return this.a.gn(0)},
C(a,b){var s=this.a
if(s.b==null)s=s.gD().C(0,b)
else{s=s.a3()
if(!(b<s.length))return A.u(s,b)
s=s[b]}return s},
gt(a){var s=this.a
if(s.b==null){s=s.gD()
s=s.gt(s)}else{s=s.a3()
s=new J.at(s,s.length,A.aq(s).h("at<1>"))}return s}}
A.cg.prototype={}
A.ci.prototype={}
A.bj.prototype={
j(a){var s=A.cj(this.a)
return(this.b!=null?"Converting object to an encodable object failed:":"Converting object did not return an encodable object:")+" "+s}}
A.cq.prototype={
j(a){return"Cyclic error in JSON stringify"}}
A.dk.prototype={
bK(a,b){var s=A.iK(a,this.gbL().a)
return s},
b4(a,b){var s=A.hU(a,this.gbM().b,null)
return s},
gbM(){return B.A},
gbL(){return B.z}}
A.dm.prototype={}
A.dl.prototype={}
A.dW.prototype={
bc(a){var s,r,q,p,o,n,m=a.length
for(s=this.c,r=0,q=0;q<m;++q){p=a.charCodeAt(q)
if(p>92){if(p>=55296){o=p&64512
if(o===55296){n=q+1
n=!(n<m&&(a.charCodeAt(n)&64512)===56320)}else n=!1
if(!n)if(o===56320){o=q-1
o=!(o>=0&&(a.charCodeAt(o)&64512)===55296)}else o=!1
else o=!0
if(o){if(q>r)s.a+=B.c.P(a,r,q)
r=q+1
o=A.z(92)
s.a+=o
o=A.z(117)
s.a+=o
o=A.z(100)
s.a+=o
o=p>>>8&15
o=A.z(o<10?48+o:87+o)
s.a+=o
o=p>>>4&15
o=A.z(o<10?48+o:87+o)
s.a+=o
o=p&15
o=A.z(o<10?48+o:87+o)
s.a+=o}}continue}if(p<32){if(q>r)s.a+=B.c.P(a,r,q)
r=q+1
o=A.z(92)
s.a+=o
switch(p){case 8:o=A.z(98)
s.a+=o
break
case 9:o=A.z(116)
s.a+=o
break
case 10:o=A.z(110)
s.a+=o
break
case 12:o=A.z(102)
s.a+=o
break
case 13:o=A.z(114)
s.a+=o
break
default:o=A.z(117)
s.a+=o
o=A.z(48)
s.a=(s.a+=o)+o
o=p>>>4&15
o=A.z(o<10?48+o:87+o)
s.a+=o
o=p&15
o=A.z(o<10?48+o:87+o)
s.a+=o
break}}else if(p===34||p===92){if(q>r)s.a+=B.c.P(a,r,q)
r=q+1
o=A.z(92)
s.a+=o
o=A.z(p)
s.a+=o}}if(r===0)s.a+=a
else if(r<m)s.a+=B.c.P(a,r,m)},
ae(a){var s,r,q,p
for(s=this.a,r=s.length,q=0;q<r;++q){p=s[q]
if(a==null?p==null:a===p)throw A.c(new A.cq(a,null))}B.a.p(s,a)},
ab(a){var s,r,q,p,o=this
if(o.bb(a))return
o.ae(a)
try{s=o.b.$1(a)
if(!o.bb(s)){q=A.fd(a,null,o.gaS())
throw A.c(q)}q=o.a
if(0>=q.length)return A.u(q,-1)
q.pop()}catch(p){r=A.I(p)
q=A.fd(a,r,o.gaS())
throw A.c(q)}},
bb(a){var s,r,q=this
if(typeof a=="number"){if(!isFinite(a))return!1
q.c.a+=B.w.j(a)
return!0}else if(a===!0){q.c.a+="true"
return!0}else if(a===!1){q.c.a+="false"
return!0}else if(a==null){q.c.a+="null"
return!0}else if(typeof a=="string"){s=q.c
s.a+='"'
q.bc(a)
s.a+='"'
return!0}else if(t.j.b(a)){q.ae(a)
q.bX(a)
s=q.a
if(0>=s.length)return A.u(s,-1)
s.pop()
return!0}else if(t.f.b(a)){q.ae(a)
r=q.bY(a)
s=q.a
if(0>=s.length)return A.u(s,-1)
s.pop()
return r}else return!1},
bX(a){var s,r,q=this.c
q.a+="["
s=J.d4(a)
if(s.gJ(a)){this.ab(s.i(a,0))
for(r=1;r<s.gn(a);++r){q.a+=","
this.ab(s.i(a,r))}}q.a+="]"},
bY(a){var s,r,q,p,o,n,m=this,l={}
if(a.gu(a)){m.c.a+="{}"
return!0}s=a.gn(a)*2
r=A.ff(s,null,!1,t.X)
q=l.a=0
l.b=!0
a.G(0,new A.dX(l,r))
if(!l.b)return!1
p=m.c
p.a+="{"
for(o='"';q<s;q+=2,o=',"'){p.a+=o
m.bc(A.C(r[q]))
p.a+='":'
n=q+1
if(!(n<s))return A.u(r,n)
m.ab(r[n])}p.a+="}"
return!0}}
A.dX.prototype={
$2(a,b){var s,r
if(typeof a!="string")this.a.b=!1
s=this.b
r=this.a
B.a.B(s,r.a++,a)
B.a.B(s,r.a++,b)},
$S:9}
A.dV.prototype={
gaS(){var s=this.c.a
return s.charCodeAt(0)==0?s:s}}
A.p.prototype={
gO(){return A.hH(this)}}
A.cc.prototype={
j(a){var s=this.a
if(s!=null)return"Assertion failed: "+A.cj(s)
return"Assertion failed"}}
A.a8.prototype={}
A.a3.prototype={
gaj(){return"Invalid argument"+(!this.a?"(s)":"")},
gai(){return""},
j(a){var s=this,r=s.c,q=r==null?"":" ("+r+")",p=s.d,o=p==null?"":": "+p,n=s.gaj()+q+o
if(!s.a)return n
return n+s.gai()+": "+A.cj(s.gaz())},
gaz(){return this.b}}
A.bu.prototype={
gaz(){return A.fE(this.b)},
gaj(){return"RangeError"},
gai(){var s,r=this.e,q=this.f
if(r==null)s=q!=null?": Not less than or equal to "+A.m(q):""
else if(q==null)s=": Not greater than or equal to "+A.m(r)
else if(q>r)s=": Not in inclusive range "+A.m(r)+".."+A.m(q)
else s=q<r?": Valid value range is empty":": Only valid value is "+A.m(r)
return s}}
A.ck.prototype={
gaz(){return A.L(this.b)},
gaj(){return"RangeError"},
gai(){if(A.L(this.b)<0)return": index must not be negative"
var s=this.f
if(s===0)return": no indices are valid"
return": index should be less than "+s},
gn(a){return this.f}}
A.by.prototype={
j(a){return"Unsupported operation: "+this.a}}
A.cI.prototype={
j(a){return"UnimplementedError: "+this.a}}
A.am.prototype={
j(a){return"Bad state: "+this.a}}
A.ch.prototype={
j(a){var s=this.a
if(s==null)return"Concurrent modification during iteration."
return"Concurrent modification during iteration: "+A.cj(s)+"."}}
A.cz.prototype={
j(a){return"Out of Memory"},
gO(){return null},
$ip:1}
A.bw.prototype={
j(a){return"Stack Overflow"},
gO(){return null},
$ip:1}
A.aA.prototype={
j(a){return"Exception: "+this.a}}
A.da.prototype={
j(a){var s=this.a,r=""!==s?"FormatException: "+s:"FormatException"
return r}}
A.b.prototype={
a6(a,b){return A.hl(this,A.e(this).h("b.E"),b)},
X(a,b,c){var s=A.e(this)
return A.hF(this,s.l(c).h("1(b.E)").a(b),s.h("b.E"),c)},
aF(a,b){return new A.aa(this,b.h("aa<0>"))},
b7(a,b){var s,r,q=this.gt(this)
if(!q.k())return""
s=J.ah(q.gm())
if(!q.k())return s
if(b.length===0){r=s
do r+=J.ah(q.gm())
while(q.k())}else{r=s
do r=r+b+J.ah(q.gm())
while(q.k())}return r.charCodeAt(0)==0?r:r},
gn(a){var s,r=this.gt(this)
for(s=0;r.k();)++s
return s},
gu(a){return!this.gt(this).k()},
gJ(a){return!this.gu(this)},
C(a,b){var s,r=this.gt(this)
for(s=b;r.k();){if(s===0)return r.gm();--s}throw A.c(A.fa(b,b-s,this,"index"))},
j(a){return A.hv(this,"(",")")}}
A.F.prototype={
gA(a){return A.f.prototype.gA.call(this,0)},
j(a){return"null"}}
A.f.prototype={$if:1,
H(a,b){return this===b},
gA(a){return A.bt(this)},
j(a){return"Instance of '"+A.cB(this)+"'"},
gv(a){return A.j6(this)},
toString(){return this.j(this)}}
A.cV.prototype={
j(a){return""},
$iT:1}
A.aT.prototype={
gn(a){return this.a.length},
j(a){var s=this.a
return s.charCodeAt(0)==0?s:s},
$ihM:1}
A.ds.prototype={
j(a){return"Promise was rejected with a value of `"+(this.a?"undefined":"null")+"`."}}
A.eo.prototype={
$1(a){var s,r,q,p
if(A.fM(a))return a
s=this.a
if(s.W(a))return s.i(0,a)
if(t.f.b(a)){r={}
s.B(0,a,r)
for(s=a.gD(),s=s.gt(s);s.k();){q=s.gm()
r[q]=this.$1(a.i(0,q))}return r}else if(t.U.b(a)){p=[]
s.B(0,a,p)
B.a.bG(p,J.hi(a,this,t.z))
return p}else return a},
$S:20}
A.ey.prototype={
$1(a){return this.a.V(this.b.h("0/?").a(a))},
$S:2}
A.ez.prototype={
$1(a){if(a==null)return this.a.N(new A.ds(a===undefined))
return this.a.N(a)},
$S:2}
A.aO.prototype={}
A.Q.prototype={}
A.eb.prototype={
$1(a){return J.P(t.f.a(a).i(0,"type"),"text")},
$S:4}
A.ec.prototype={
$1(a){return A.C(t.f.a(a).i(0,"text"))},
$S:10}
A.eq.prototype={
$1(a){t.f.a(a)
return J.P(a.i(0,"role"),"user")||J.P(a.i(0,"role"),"assistant")},
$S:4}
A.er.prototype={
$1(a){t.f.a(a)
return new A.Q(A.C(a.i(0,"role")),A.il(t.P.a(a)))},
$S:21}
A.es.prototype={
$1(a){return t.E.a(a).b.length!==0},
$S:22}
A.eC.prototype={
$1(a){var s,r,q,p,o,n,m,l,k,j,i,h,g,f,e,d=this,c=null,b="state"
t.P.a(a)
s=A.a1(a.i(0,"event"))
r=t.h.a(a.i(0,"payload"))
if(r==null)r=A.dp(t.N,t.z)
if(s==="agent"&&J.P(r.i(0,"stream"),"assistant")){q=t.Y.a(r.i(0,"data"))
if(q==null){p=t.z
q=A.dp(p,p)}o=A.a1(q.i(0,"delta"))
if(o==null)o=""
n=t.g.a(q.i(0,"mediaUrls"))
m=n==null?c:J.hf(n,t.N)
if(m==null)m=A.Y([],t.s)
if(o.length!==0||J.f2(m))d.a.p(0,new A.aO(o,!1,m))}p=s==="chat"
if(p&&J.P(r.i(0,b),"final")){l=t.Y.a(r.i(0,"message"))
k=l==null
j=k?c:l.i(0,"content")
t.g.a(j)
if(j==null)i=c
else{j=J.eE(j,t.f)
h=j.$ti
h=new A.E(new A.U(j,h.h("G(b.E)").a(new A.eA()),h.h("U<b.E>")),h.h("j(b.E)").a(new A.eB()),h.h("E<b.E,j>")).b7(0,"")
i=h}if(i==null)i=""
A.a1(k?c:l.i(0,"voice"))
j=d.a
j.p(0,new A.aO(i,!0,B.B))
d.b.aU().F()
j.b3()}if(p)p=J.P(r.i(0,b),"error")||J.P(r.i(0,b),"aborted")
else p=!1
if(p){p=d.a
k=A.m(r.i(0,b))
if(p.b>=4)A.b3(p.ac())
g=A.fH(new A.aA("Chat "+k),c)
f=g.a
e=g.b
k=p.b
if((k&1)!==0)p.au(f,e)
else if((k&3)===0)p.ah().p(0,new A.bH(f,e))
d.b.aU().F()
p.b3()}},
$S:23}
A.eA.prototype={
$1(a){return J.P(t.f.a(a).i(0,"type"),"text")},
$S:4}
A.eB.prototype={
$1(a){return A.C(t.f.a(a).i(0,"text"))},
$S:10}
A.db.prototype={
bJ(){var s,r,q=this,p=new A.i($.h,t.k),o=new A.ab(p,t.cp),n=v.G.WebSocket,m=$.h0().i(0,"wsUrl")
m.toString
m=A.q(new n(m))
q.a=m
n=q.e
s=t.bj
r=t.m
B.a.p(n,A.aW(m,"open",s.a(new A.dc()),!1,r))
m=q.a
m.toString
B.a.p(n,A.aW(m,"message",s.a(new A.dd(q,o)),!1,r))
m=q.a
m.toString
B.a.p(n,A.aW(m,"error",s.a(new A.de(o)),!1,r))
m=q.a
m.toString
B.a.p(n,A.aW(m,"close",s.a(new A.df(q)),!1,r))
return p},
bn(a,b){var s,r,q,p,o,n=this
t.P.a(a)
t.r.a(b)
s=A.a1(a.i(0,"type"))
A.a1(a.i(0,"event"))
r=s==="res"
if(r&&J.P(a.i(0,"ok"),!0)){q=t.Y.a(a.i(0,"payload"))
p=q==null?null:q.i(0,"type")
q=J.ar(p)
if(q.H(p,"hello-ok")||q.H(p,"hello")){n.b=!0
if((b.a.a&30)===0)b.V(!0)
return}}if(r&&J.P(a.i(0,"ok"),!1)){if((b.a.a&30)===0)b.N(new A.aA(A.m(a.i(0,"error"))))
return}if(r){o=A.a1(a.i(0,"id"))
if(o!=null&&n.d.W(o)){r=n.d.bS(0,o)
r.toString
if(J.P(a.i(0,"ok"),!0)){q=t.h.a(a.i(0,"payload"))
r.V(q==null?A.dp(t.N,t.z):q)}else r.N(new A.aA(A.m(a.i(0,"error"))))
return}}if(s==="event"){r=n.c
A.e(r).c.a(a)
if(!r.gbp())A.b3(r.bg())
r.U(a)}},
aG(a){var s
t.P.a(a)
s=this.a
if(s!=null)s.send(B.f.b4(a,null))}}
A.dc.prototype={
$1(a){A.H("[ws] WebSocket opened")},
$S:1}
A.dd.prototype={
$1(a){var s=A.C(a.data),r=t.P.a(B.f.bK(s,null)),q=A.a1(r.i(0,"event"))
if(q!=="tick"&&q!=="health")A.H("[ws] recv: "+(s.length>500?B.c.P(s,0,500):s))
this.a.bn(r,this.b)},
$S:1}
A.de.prototype={
$1(a){var s
A.H("[ws] WebSocket error")
s=this.a
if((s.a.a&30)===0)s.N(new A.aA("WebSocket error"))},
$S:1}
A.df.prototype={
$1(a){A.H("[ws] WebSocket closed: code="+A.L(a.code)+" reason="+A.C(a.reason))
this.a.b=!1},
$S:1}
A.eG.prototype={}
A.bJ.prototype={
a8(a,b,c,d){var s=A.e(this)
s.h("~(1)?").a(a)
t.Z.a(c)
return A.aW(this.a,this.b,a,!1,s.c)}}
A.cO.prototype={}
A.bK.prototype={
F(){var s=this,r=A.f9(null,t.H)
if(s.b==null)return r
s.b1()
s.d=s.b=null
return r},
a9(){if(this.b==null)return;++this.a
this.b1()},
Z(){var s=this
if(s.b==null||s.a<=0)return;--s.a
s.b0()},
b0(){var s=this,r=s.d
if(r!=null&&s.a<=0)s.b.addEventListener(s.c,r,!1)},
b1(){var s=this.d
if(s!=null)this.b.removeEventListener(this.c,s,!1)},
$iK:1}
A.dJ.prototype={
$1(a){return this.a.$1(A.q(a))},
$S:1}
A.et.prototype={
$1(a){return A.ca()},
$S:1}
A.eu.prototype={
$1(a){if(A.C(a.key)==="Enter")A.ca()},
$S:1};(function aliases(){var s=J.ak.prototype
s.be=s.j})();(function installTearOffs(){var s=hunkHelpers._static_1,r=hunkHelpers._static_0,q=hunkHelpers._static_2,p=hunkHelpers._instance_0u,o=hunkHelpers._instance_2u,n=hunkHelpers._instance_1u
s(A,"iY","hO",5)
s(A,"iZ","hP",5)
s(A,"j_","hQ",5)
r(A,"fU","iR",0)
q(A,"j0","iJ",3)
r(A,"fT","iI",0)
var m
p(m=A.a_.prototype,"gao","L",0)
p(m,"gap","M",0)
o(A.i.prototype,"gbi","bj",3)
p(m=A.ac.prototype,"gao","L",0)
p(m,"gap","M",0)
p(m=A.az.prototype,"gao","L",0)
p(m,"gap","M",0)
p(A.aV.prototype,"gaR","bw",0)
n(m=A.aD.prototype,"gbq","br",18)
o(m,"gbu","bv",3)
p(m,"gbs","bt",0)
s(A,"j2","ij",6)})();(function inheritance(){var s=hunkHelpers.mixin,r=hunkHelpers.inherit,q=hunkHelpers.inheritMany
r(A.f,null)
q(A.f,[A.eH,J.cl,A.bv,J.at,A.b,A.b7,A.p,A.ai,A.ay,A.bm,A.bz,A.bA,A.D,A.b9,A.bQ,A.dw,A.dt,A.bc,A.bV,A.y,A.dn,A.bk,A.dI,A.cW,A.S,A.cQ,A.e4,A.e2,A.bB,A.A,A.a7,A.az,A.bE,A.bG,A.af,A.i,A.cK,A.bW,A.cL,A.ae,A.cN,A.W,A.aV,A.aD,A.c1,A.bN,A.l,A.cg,A.ci,A.dW,A.cz,A.bw,A.aA,A.da,A.F,A.cV,A.aT,A.ds,A.aO,A.Q,A.db,A.eG,A.bK])
q(J.cl,[J.cn,J.be,J.bh,J.bg,J.bi,J.bf,J.aQ])
q(J.bh,[J.ak,J.x,A.al,A.bp])
q(J.ak,[J.cA,J.bx,J.aj])
r(J.cm,A.bv)
r(J.dj,J.x)
q(J.bf,[J.bd,J.co])
q(A.b,[A.an,A.d,A.E,A.U,A.aa,A.bP])
q(A.an,[A.au,A.c2])
r(A.bI,A.au)
r(A.bF,A.c2)
r(A.a4,A.bF)
q(A.p,[A.aw,A.a8,A.cp,A.cJ,A.cD,A.cP,A.bj,A.cc,A.a3,A.by,A.cI,A.am,A.ch])
q(A.ai,[A.ce,A.cf,A.cH,A.ek,A.em,A.dD,A.dC,A.e8,A.dS,A.du,A.e_,A.eo,A.ey,A.ez,A.eb,A.ec,A.eq,A.er,A.es,A.eC,A.eA,A.eB,A.dc,A.dd,A.de,A.df,A.dJ,A.et,A.eu])
q(A.ce,[A.ew,A.dE,A.dF,A.e3,A.dK,A.dO,A.dN,A.dM,A.dL,A.dR,A.dQ,A.dP,A.dv,A.e1,A.e0,A.dH,A.dG,A.dY,A.dZ,A.ee])
q(A.d,[A.R,A.ax,A.bM])
r(A.bb,A.E)
q(A.R,[A.a6,A.cS])
r(A.ba,A.b9)
r(A.bs,A.a8)
q(A.cH,[A.cF,A.aN])
q(A.y,[A.a5,A.bL,A.cR])
q(A.cf,[A.el,A.e9,A.ef,A.dT,A.dq,A.dr,A.dX])
r(A.aR,A.al)
q(A.bp,[A.cr,A.aS])
q(A.aS,[A.bR,A.bT])
r(A.bS,A.bR)
r(A.bn,A.bS)
r(A.bU,A.bT)
r(A.bo,A.bU)
q(A.bn,[A.cs,A.ct])
q(A.bo,[A.cu,A.cv,A.cw,A.cx,A.cy,A.bq,A.br])
r(A.bY,A.cP)
q(A.a7,[A.aX,A.bJ])
r(A.ao,A.aX)
r(A.bD,A.ao)
r(A.ac,A.az)
r(A.a_,A.ac)
r(A.bC,A.bE)
r(A.ab,A.bG)
r(A.aU,A.bW)
q(A.ae,[A.ad,A.bH])
r(A.cT,A.c1)
r(A.bO,A.bL)
r(A.cq,A.bj)
r(A.dk,A.cg)
q(A.ci,[A.dm,A.dl])
r(A.dV,A.dW)
q(A.a3,[A.bu,A.ck])
r(A.cO,A.bJ)
s(A.c2,A.l)
s(A.bR,A.l)
s(A.bS,A.D)
s(A.bT,A.l)
s(A.bU,A.D)
s(A.aU,A.cL)})()
var v={G:typeof self!="undefined"?self:globalThis,typeUniverse:{eC:new Map(),tR:{},eT:{},tPV:{},sEA:[]},mangledGlobalNames:{a:"int",o:"double",aL:"num",j:"String",G:"bool",F:"Null",k:"List",f:"Object",t:"Map",r:"JSObject"},mangledNames:{},types:["~()","~(r)","~(@)","~(f,T)","G(t<@,@>)","~(~())","@(@)","F(@)","F()","~(f?,f?)","j(t<@,@>)","Z<~>()","@(@,j)","@(j)","F(~())","F(@,T)","~(a,@)","F(f,T)","~(f?)","~(@,@)","f?(f?)","Q(t<@,@>)","G(Q)","~(t<j,@>)"],interceptorsByTag:null,leafTags:null,arrayRti:Symbol("$ti")}
A.i7(v.typeUniverse,JSON.parse('{"cA":"ak","bx":"ak","aj":"ak","js":"al","cn":{"G":[],"n":[]},"be":{"n":[]},"bh":{"r":[]},"ak":{"r":[]},"x":{"k":["1"],"d":["1"],"r":[],"b":["1"]},"cm":{"bv":[]},"dj":{"x":["1"],"k":["1"],"d":["1"],"r":[],"b":["1"]},"at":{"B":["1"]},"bf":{"o":[],"aL":[]},"bd":{"o":[],"a":[],"aL":[],"n":[]},"co":{"o":[],"aL":[],"n":[]},"aQ":{"j":[],"n":[]},"an":{"b":["2"]},"b7":{"B":["2"]},"au":{"an":["1","2"],"b":["2"],"b.E":"2"},"bI":{"au":["1","2"],"an":["1","2"],"d":["2"],"b":["2"],"b.E":"2"},"bF":{"l":["2"],"k":["2"],"an":["1","2"],"d":["2"],"b":["2"]},"a4":{"bF":["1","2"],"l":["2"],"k":["2"],"an":["1","2"],"d":["2"],"b":["2"],"l.E":"2","b.E":"2"},"aw":{"p":[]},"d":{"b":["1"]},"R":{"d":["1"],"b":["1"]},"ay":{"B":["1"]},"E":{"b":["2"],"b.E":"2"},"bb":{"E":["1","2"],"d":["2"],"b":["2"],"b.E":"2"},"bm":{"B":["2"]},"a6":{"R":["2"],"d":["2"],"b":["2"],"b.E":"2","R.E":"2"},"U":{"b":["1"],"b.E":"1"},"bz":{"B":["1"]},"aa":{"b":["1"],"b.E":"1"},"bA":{"B":["1"]},"b9":{"t":["1","2"]},"ba":{"b9":["1","2"],"t":["1","2"]},"bP":{"b":["1"],"b.E":"1"},"bQ":{"B":["1"]},"bs":{"a8":[],"p":[]},"cp":{"p":[]},"cJ":{"p":[]},"bV":{"T":[]},"ai":{"av":[]},"ce":{"av":[]},"cf":{"av":[]},"cH":{"av":[]},"cF":{"av":[]},"aN":{"av":[]},"cD":{"p":[]},"a5":{"y":["1","2"],"fe":["1","2"],"t":["1","2"],"y.K":"1","y.V":"2"},"ax":{"d":["1"],"b":["1"],"b.E":"1"},"bk":{"B":["1"]},"aR":{"al":[],"r":[],"b6":[],"n":[]},"al":{"r":[],"b6":[],"n":[]},"bp":{"r":[]},"cW":{"b6":[]},"cr":{"eF":[],"r":[],"n":[]},"aS":{"J":["1"],"r":[]},"bn":{"l":["o"],"k":["o"],"J":["o"],"d":["o"],"r":[],"b":["o"],"D":["o"]},"bo":{"l":["a"],"k":["a"],"J":["a"],"d":["a"],"r":[],"b":["a"],"D":["a"]},"cs":{"d8":[],"l":["o"],"k":["o"],"J":["o"],"d":["o"],"r":[],"b":["o"],"D":["o"],"n":[],"l.E":"o"},"ct":{"d9":[],"l":["o"],"k":["o"],"J":["o"],"d":["o"],"r":[],"b":["o"],"D":["o"],"n":[],"l.E":"o"},"cu":{"dg":[],"l":["a"],"k":["a"],"J":["a"],"d":["a"],"r":[],"b":["a"],"D":["a"],"n":[],"l.E":"a"},"cv":{"dh":[],"l":["a"],"k":["a"],"J":["a"],"d":["a"],"r":[],"b":["a"],"D":["a"],"n":[],"l.E":"a"},"cw":{"di":[],"l":["a"],"k":["a"],"J":["a"],"d":["a"],"r":[],"b":["a"],"D":["a"],"n":[],"l.E":"a"},"cx":{"dy":[],"l":["a"],"k":["a"],"J":["a"],"d":["a"],"r":[],"b":["a"],"D":["a"],"n":[],"l.E":"a"},"cy":{"dz":[],"l":["a"],"k":["a"],"J":["a"],"d":["a"],"r":[],"b":["a"],"D":["a"],"n":[],"l.E":"a"},"bq":{"dA":[],"l":["a"],"k":["a"],"J":["a"],"d":["a"],"r":[],"b":["a"],"D":["a"],"n":[],"l.E":"a"},"br":{"dB":[],"l":["a"],"k":["a"],"J":["a"],"d":["a"],"r":[],"b":["a"],"D":["a"],"n":[],"l.E":"a"},"cP":{"p":[]},"bY":{"a8":[],"p":[]},"bB":{"b8":["1"]},"A":{"p":[]},"bD":{"ao":["1"],"aX":["1"],"a7":["1"]},"a_":{"ac":["1"],"az":["1"],"K":["1"],"V":["1"]},"bE":{"cG":["1"],"cU":["1"],"V":["1"]},"bC":{"bE":["1"],"cG":["1"],"cU":["1"],"V":["1"]},"bG":{"b8":["1"]},"ab":{"bG":["1"],"b8":["1"]},"i":{"Z":["1"]},"bW":{"cG":["1"],"cU":["1"],"V":["1"]},"aU":{"cL":["1"],"bW":["1"],"cG":["1"],"cU":["1"],"V":["1"]},"ao":{"aX":["1"],"a7":["1"]},"ac":{"az":["1"],"K":["1"],"V":["1"]},"az":{"K":["1"],"V":["1"]},"aX":{"a7":["1"]},"ad":{"ae":["1"]},"bH":{"ae":["@"]},"cN":{"ae":["@"]},"aV":{"K":["1"]},"c1":{"fn":[]},"cT":{"c1":[],"fn":[]},"bL":{"y":["1","2"],"t":["1","2"]},"bO":{"bL":["1","2"],"y":["1","2"],"t":["1","2"],"y.K":"1","y.V":"2"},"bM":{"d":["1"],"b":["1"],"b.E":"1"},"bN":{"B":["1"]},"y":{"t":["1","2"]},"cR":{"y":["j","@"],"t":["j","@"],"y.K":"j","y.V":"@"},"cS":{"R":["j"],"d":["j"],"b":["j"],"b.E":"j","R.E":"j"},"bj":{"p":[]},"cq":{"p":[]},"o":{"aL":[]},"a":{"aL":[]},"k":{"d":["1"],"b":["1"]},"cc":{"p":[]},"a8":{"p":[]},"a3":{"p":[]},"bu":{"p":[]},"ck":{"p":[]},"by":{"p":[]},"cI":{"p":[]},"am":{"p":[]},"ch":{"p":[]},"cz":{"p":[]},"bw":{"p":[]},"cV":{"T":[]},"aT":{"hM":[]},"bJ":{"a7":["1"]},"cO":{"bJ":["1"],"a7":["1"]},"bK":{"K":["1"]},"di":{"k":["a"],"d":["a"],"b":["a"]},"dB":{"k":["a"],"d":["a"],"b":["a"]},"dA":{"k":["a"],"d":["a"],"b":["a"]},"dg":{"k":["a"],"d":["a"],"b":["a"]},"dy":{"k":["a"],"d":["a"],"b":["a"]},"dh":{"k":["a"],"d":["a"],"b":["a"]},"dz":{"k":["a"],"d":["a"],"b":["a"]},"d8":{"k":["o"],"d":["o"],"b":["o"]},"d9":{"k":["o"],"d":["o"],"b":["o"]}}'))
A.i6(v.typeUniverse,JSON.parse('{"c2":2,"aS":1,"ae":1,"cg":2,"ci":2}'))
var u={c:"Error handler must accept one Object or one Object and a StackTrace as arguments, and return a value of the returned future's type"}
var t=(function rtii(){var s=A.aI
return{p:s("@<~>"),n:s("A"),J:s("b6"),V:s("eF"),r:s("b8<G>"),R:s("d<@>"),C:s("p"),B:s("d8"),W:s("d9"),b:s("av"),E:s("Q"),c:s("dg"),t:s("dh"),G:s("di"),U:s("b<@>"),s:s("x<j>"),w:s("x<@>"),T:s("be"),m:s("r"),L:s("aj"),d:s("J<@>"),x:s("k<Q>"),j:s("k<@>"),P:s("t<j,@>"),f:s("t<@,@>"),q:s("aR"),a:s("F"),K:s("f"),cY:s("jt"),l:s("T"),N:s("j"),bW:s("n"),b7:s("a8"),c0:s("dy"),bk:s("dz"),ca:s("dA"),bX:s("dB"),cr:s("bx"),cS:s("ab<t<j,@>>"),cp:s("ab<G>"),d6:s("aU<aO>"),bU:s("cO<r>"),cU:s("i<t<j,@>>"),k:s("i<G>"),_:s("i<@>"),aQ:s("i<a>"),D:s("i<~>"),A:s("bO<f?,f?>"),cN:s("bX<f?>"),a4:s("aD<aO>"),y:s("G"),bG:s("G(f)"),i:s("o"),z:s("@"),O:s("@()"),v:s("@(f)"),Q:s("@(f,T)"),S:s("a"),bc:s("Z<F>?"),b1:s("r?"),g:s("k<@>?"),h:s("t<j,@>?"),Y:s("t<@,@>?"),X:s("f?"),aD:s("j?"),cd:s("ae<@>?"),F:s("af<@,@>?"),cG:s("G?"),I:s("o?"),a3:s("a?"),ae:s("aL?"),Z:s("~()?"),bj:s("~(r)?"),o:s("aL"),H:s("~"),M:s("~()"),u:s("~(f)"),e:s("~(f,T)"),cQ:s("~(j,@)")}})();(function constants(){var s=hunkHelpers.makeConstList
B.v=J.cl.prototype
B.a=J.x.prototype
B.e=J.bd.prototype
B.w=J.bf.prototype
B.c=J.aQ.prototype
B.x=J.aj.prototype
B.y=J.bh.prototype
B.C=A.br.prototype
B.m=J.cA.prototype
B.h=J.bx.prototype
B.i=function getTagFallback(o) {
  var s = Object.prototype.toString.call(o);
  return s.substring(8, s.length - 1);
}
B.n=function() {
  var toStringFunction = Object.prototype.toString;
  function getTag(o) {
    var s = toStringFunction.call(o);
    return s.substring(8, s.length - 1);
  }
  function getUnknownTag(object, tag) {
    if (/^HTML[A-Z].*Element$/.test(tag)) {
      var name = toStringFunction.call(object);
      if (name == "[object Object]") return null;
      return "HTMLElement";
    }
  }
  function getUnknownTagGenericBrowser(object, tag) {
    if (object instanceof HTMLElement) return "HTMLElement";
    return getUnknownTag(object, tag);
  }
  function prototypeForTag(tag) {
    if (typeof window == "undefined") return null;
    if (typeof window[tag] == "undefined") return null;
    var constructor = window[tag];
    if (typeof constructor != "function") return null;
    return constructor.prototype;
  }
  function discriminator(tag) { return null; }
  var isBrowser = typeof HTMLElement == "function";
  return {
    getTag: getTag,
    getUnknownTag: isBrowser ? getUnknownTagGenericBrowser : getUnknownTag,
    prototypeForTag: prototypeForTag,
    discriminator: discriminator };
}
B.t=function(getTagFallback) {
  return function(hooks) {
    if (typeof navigator != "object") return hooks;
    var userAgent = navigator.userAgent;
    if (typeof userAgent != "string") return hooks;
    if (userAgent.indexOf("DumpRenderTree") >= 0) return hooks;
    if (userAgent.indexOf("Chrome") >= 0) {
      function confirm(p) {
        return typeof window == "object" && window[p] && window[p].name == p;
      }
      if (confirm("Window") && confirm("HTMLElement")) return hooks;
    }
    hooks.getTag = getTagFallback;
  };
}
B.o=function(hooks) {
  if (typeof dartExperimentalFixupGetTag != "function") return hooks;
  hooks.getTag = dartExperimentalFixupGetTag(hooks.getTag);
}
B.r=function(hooks) {
  if (typeof navigator != "object") return hooks;
  var userAgent = navigator.userAgent;
  if (typeof userAgent != "string") return hooks;
  if (userAgent.indexOf("Firefox") == -1) return hooks;
  var getTag = hooks.getTag;
  var quickMap = {
    "BeforeUnloadEvent": "Event",
    "DataTransfer": "Clipboard",
    "GeoGeolocation": "Geolocation",
    "Location": "!Location",
    "WorkerMessageEvent": "MessageEvent",
    "XMLDocument": "!Document"};
  function getTagFirefox(o) {
    var tag = getTag(o);
    return quickMap[tag] || tag;
  }
  hooks.getTag = getTagFirefox;
}
B.q=function(hooks) {
  if (typeof navigator != "object") return hooks;
  var userAgent = navigator.userAgent;
  if (typeof userAgent != "string") return hooks;
  if (userAgent.indexOf("Trident/") == -1) return hooks;
  var getTag = hooks.getTag;
  var quickMap = {
    "BeforeUnloadEvent": "Event",
    "DataTransfer": "Clipboard",
    "HTMLDDElement": "HTMLElement",
    "HTMLDTElement": "HTMLElement",
    "HTMLPhraseElement": "HTMLElement",
    "Position": "Geoposition"
  };
  function getTagIE(o) {
    var tag = getTag(o);
    var newTag = quickMap[tag];
    if (newTag) return newTag;
    if (tag == "Object") {
      if (window.DataView && (o instanceof window.DataView)) return "DataView";
    }
    return tag;
  }
  function prototypeForTagIE(tag) {
    var constructor = window[tag];
    if (constructor == null) return null;
    return constructor.prototype;
  }
  hooks.getTag = getTagIE;
  hooks.prototypeForTag = prototypeForTagIE;
}
B.p=function(hooks) {
  var getTag = hooks.getTag;
  var prototypeForTag = hooks.prototypeForTag;
  function getTagFixed(o) {
    var tag = getTag(o);
    if (tag == "Document") {
      if (!!o.xmlVersion) return "!Document";
      return "!HTMLDocument";
    }
    return tag;
  }
  function prototypeForTagFixed(tag) {
    if (tag == "Document") return null;
    return prototypeForTag(tag);
  }
  hooks.getTag = getTagFixed;
  hooks.prototypeForTag = prototypeForTagFixed;
}
B.j=function(hooks) { return hooks; }

B.f=new A.dk()
B.u=new A.cz()
B.k=new A.cN()
B.b=new A.cT()
B.d=new A.cV()
B.z=new A.dl(null)
B.A=new A.dm(null)
B.B=s([],t.s)
B.D={wsUrl:0}
B.l=new A.ba(B.D,[""],A.aI("ba<j,j>"))
B.E=A.a2("b6")
B.F=A.a2("eF")
B.G=A.a2("d8")
B.H=A.a2("d9")
B.I=A.a2("dg")
B.J=A.a2("dh")
B.K=A.a2("di")
B.L=A.a2("dy")
B.M=A.a2("dz")
B.N=A.a2("dA")
B.O=A.a2("dB")})();(function staticFields(){$.dU=null
$.N=A.Y([],A.aI("x<f>"))
$.fg=null
$.f6=null
$.f5=null
$.fW=null
$.fS=null
$.fZ=null
$.ej=null
$.en=null
$.eT=null
$.aZ=null
$.c5=null
$.c6=null
$.eQ=!1
$.h=B.b
$.c3=A.cM()
$.cX=A.cM()
$.c4=A.cM()
$.X=A.cM()})();(function lazyInitializers(){var s=hunkHelpers.lazyFinal
s($,"jp","f_",()=>A.j5("_$dart_dartClosure"))
s($,"jJ","hd",()=>B.b.b8(new A.ew(),A.aI("Z<~>")))
s($,"jG","hc",()=>A.Y([new J.cm()],A.aI("x<bv>")))
s($,"jv","h2",()=>A.a9(A.dx({
toString:function(){return"$receiver$"}})))
s($,"jw","h3",()=>A.a9(A.dx({$method$:null,
toString:function(){return"$receiver$"}})))
s($,"jx","h4",()=>A.a9(A.dx(null)))
s($,"jy","h5",()=>A.a9(function(){var $argumentsExpr$="$arguments$"
try{null.$method$($argumentsExpr$)}catch(r){return r.message}}()))
s($,"jB","h8",()=>A.a9(A.dx(void 0)))
s($,"jC","h9",()=>A.a9(function(){var $argumentsExpr$="$arguments$"
try{(void 0).$method$($argumentsExpr$)}catch(r){return r.message}}()))
s($,"jA","h7",()=>A.a9(A.fk(null)))
s($,"jz","h6",()=>A.a9(function(){try{null.$method$}catch(r){return r.message}}()))
s($,"jE","hb",()=>A.a9(A.fk(void 0)))
s($,"jD","ha",()=>A.a9(function(){try{(void 0).$method$}catch(r){return r.message}}()))
s($,"jF","f0",()=>A.hN())
s($,"jr","b4",()=>$.hd())
s($,"jq","h1",()=>{var r=new A.i(B.b,t.k)
r.bD(!1)
return r})
s($,"jo","h0",()=>A.hr())
s($,"jI","d6",()=>new A.db(new A.bC(null,null,A.aI("bC<t<j,@>>")),A.dp(t.N,A.aI("b8<t<j,@>>")),A.Y([],A.aI("x<K<@>>"))))})();(function nativeSupport(){!function(){var s=function(a){var m={}
m[a]=1
return Object.keys(hunkHelpers.convertToFastObject(m))[0]}
v.getIsolateTag=function(a){return s("___dart_"+a+v.isolateTag)}
var r="___dart_isolate_tags_"
var q=Object[r]||(Object[r]=Object.create(null))
var p="_ZxYxX"
for(var o=0;;o++){var n=s(p+"_"+o+"_")
if(!(n in q)){q[n]=1
v.isolateTag=n
break}}v.dispatchPropertyName=v.getIsolateTag("dispatch_record")}()
hunkHelpers.setOrUpdateInterceptorsByTag({SharedArrayBuffer:A.al,ArrayBuffer:A.aR,ArrayBufferView:A.bp,DataView:A.cr,Float32Array:A.cs,Float64Array:A.ct,Int16Array:A.cu,Int32Array:A.cv,Int8Array:A.cw,Uint16Array:A.cx,Uint32Array:A.cy,Uint8ClampedArray:A.bq,CanvasPixelArray:A.bq,Uint8Array:A.br})
hunkHelpers.setOrUpdateLeafTags({SharedArrayBuffer:true,ArrayBuffer:true,ArrayBufferView:false,DataView:true,Float32Array:true,Float64Array:true,Int16Array:true,Int32Array:true,Int8Array:true,Uint16Array:true,Uint32Array:true,Uint8ClampedArray:true,CanvasPixelArray:true,Uint8Array:false})
A.aS.$nativeSuperclassTag="ArrayBufferView"
A.bR.$nativeSuperclassTag="ArrayBufferView"
A.bS.$nativeSuperclassTag="ArrayBufferView"
A.bn.$nativeSuperclassTag="ArrayBufferView"
A.bT.$nativeSuperclassTag="ArrayBufferView"
A.bU.$nativeSuperclassTag="ArrayBufferView"
A.bo.$nativeSuperclassTag="ArrayBufferView"})()
Function.prototype.$0=function(){return this()}
Function.prototype.$1=function(a){return this(a)}
Function.prototype.$2=function(a,b){return this(a,b)}
Function.prototype.$3=function(a,b,c){return this(a,b,c)}
Function.prototype.$4=function(a,b,c,d){return this(a,b,c,d)}
Function.prototype.$1$0=function(){return this()}
Function.prototype.$1$1=function(a){return this(a)}
convertAllToFastObject(w)
convertToFastObject($);(function(a){if(typeof document==="undefined"){a(null)
return}if(typeof document.currentScript!="undefined"){a(document.currentScript)
return}var s=document.scripts
function onLoad(b){for(var q=0;q<s.length;++q){s[q].removeEventListener("load",onLoad,false)}a(b.target)}for(var r=0;r<s.length;++r){s[r].addEventListener("load",onLoad,false)}})(function(a){v.currentScript=a
var s=A.jg
if(typeof dartMainRunner==="function"){dartMainRunner(s,[])}else{s([])}})})()
//# sourceMappingURL=main.dart.js.map
