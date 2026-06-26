# 跨力场复合物体系构建

> 场景：蛋白用 AMBER99SB-ILDN，配体用 GAFF2，统一在 GROMACS 中模拟。

## 核心原则

GROMACS 拓扑的 include 顺序有严格要求：

```
[ defaults ]         ← 只能出现一次！来自 forcefield.itp
[ atomtypes ]        ← 可多次出现，追加新 atomtype
[ moleculetype ]     ← 每个分子一个
[ system ]           ← 只能出现一次
[ molecules ]        ← 只能出现一次
```

**关键：** `[ defaults ]` 不能重复 include，否则报错：
```
"Found a second defaults directive"
```

## 完整工作流程

### Step 1: 单独处理蛋白

```bash
mkdir -p protein
cd protein
cp ../protein.pdb .

# 用 AMBER 力场处理蛋白
echo "1" | gmx pdb2gmx -f protein.pdb -o protein.gro \
  -p protein_topol.top -ff amber99sb-ildn -water tip3p -ignh
```

`pdb2gmx` 生成的 `protein_topol.top` 包含：
- `#include "amber99sb-ildn.ff/forcefield.itp"` → `[ defaults ]` + `[ atomtypes ]`
- `#include "tip3p.itp"` → 水模型
- `#include "ions.itp"` → 离子
- `[ moleculetype ]` Protein_chain_A
- `[ system ]` / `[ molecules ]`

### Step 2: 准备配体拓扑

参照 `ligand-topology.md`，用 acpype 生成 `LIG.itp`（包含 `[ atomtypes ]` + `[ moleculetype ]`）。

### Step 3: 合并坐标

```bash
# 用 gmx insert-molecules 插入配体
gmx insert-molecules -f protein/protein.gro \
  -ci LIG.gro -nmol 1 -o complex.gro \
  -try 100 -radius 0.12
```

### Step 4: 构建统一拓扑（关键！）

```bash
# 从蛋白拓扑中提取 [moleculetype] 部分（去除重复的 include）
# 删除以下行：
#   - #include "...forcefield.itp"
#   - #include "...tip3p.itp"
#   - #include "...ions.itp"
#   - #include "...posre.itp"
#   - [ system ] ... [ molecules ]

sed -e '/#include.*forcefield/d' \
    -e '/#include.*tip3p/d' \
    -e '/#include.*ions/d' \
    -e '/#include.*posre/d' \
    -e '/POSRES_WATER/,/endif/d' \
    protein/protein_topol.top > protein_body.itp

# 编辑 protein_body.itp，删除末尾的 [ system ] 和 [ molecules ] 部分
```

**主拓扑 system.top：**
```
; Forcefield（先加载，[ defaults ] + AMBER atomtypes）
#include "amber99sb-ildn.ff/forcefield.itp"

; 配体 atomtypes（GAFF2，追加到已有 atomtypes）
#include "LIG.itp"

; 蛋白 [moleculetype]（不含 forcefield include）
#include "protein_body.itp"

; 水和离子
#include "amber99sb-ildn.ff/tip3p.itp"
#include "amber99sb-ildn.ff/ions.itp"

#ifdef POSRES
#include "posre.itp"
#endif

[ system ]
Protein-Ligand complex in water

[ molecules ]
Protein_chain_A     1
LIG                 1
```

### Step 5: 验证拓扑

```bash
cat > test.mdp << EOF
integrator = steep
nsteps = 0
EOF

gmx grompp -f test.mdp -c complex.gro -p system.top -o test.tpr -maxwarn 20
# 成功标志：grompp 无 ERROR，最多有 NOTE
```

## 常见错误

### "Found a second defaults directive"

**原因：** forcefield.itp 被 include 了两次  
**解决：** 确保 system.top 中只 include 一次 forcefield.itp；蛋白 body 中删除 forcefield include

### "moleculetype SOL is redefined"

**原因：** tip3p.itp 被 include 了两次  
**解决：** 在蛋白 body 中删除 `#include "...tip3p.itp"`

### "No such moleculetype Protein_chain_A"

**原因：** 蛋白 [moleculetype] 未正确 include  
**解决：** 确认 protein_body.itp 中包含 `[ moleculetype ]` 定义

### 蛋白 residue 编号不匹配

如果 pdb2gmx 修改了残基编号（如 protonation state 修正）：
```bash
# 检查
grep "residue" protein.gro | awk '{print $6}' | sort -u
# 对比原始 PDB
grep "ATOM" protein.pdb | awk '{print $6}' | sort -nu
```

## 力场兼容性矩阵

| 蛋白力场 | 配体力场 | 兼容性 | 说明 |
|----------|----------|:------:|------|
| AMBER99SB | GAFF / GAFF2 | ✅ | 原生兼容，同 LJ 规则 |
| AMBER14SB | GAFF / GAFF2 | ✅ | 同上 |
| CHARMM36 | CGenFF | ✅ | CHARMM 系列 |
| CHARMM36 | GAFF2 | ⚠️ | LJ 组合规则不同，需 `[ nonbond_params ]` |
| OPLS-AA | OPLS | ✅ | OPLS 系列 |
| GROMOS54A7 | ATB | ✅ | GROMOS 系列 |

**推荐：** 始终使用 AMBER 蛋白力场 + GAFF/GAFF2 配体力场，或 CHARMM 蛋白力场 + CGenFF 配体力场。
