# Bambu Lab A1 Combo — referência

Consulte novamente a documentação oficial quando versão de software ou perfil puder ter mudado.

## Hardware

- Volume de construção nominal: 256 × 256 × 256 mm.
- Bico incluído normalmente: 0,4 mm.
- Bicos opcionais documentados: 0,2, 0,6 e 0,8 mm.
- Filamento: 1,75 mm.
- A Combo inclui AMS Lite; planeje normalmente até quatro entradas de filamento.

Fonte oficial: https://cdn1.bambulab.com/documentation/quick-start-b5f1a684f77/A1%20Combo%20Quick%20Start_V0%28EN%29.pdf

Não trate todo o cubo nominal como garantia de espaço livre para qualquer geometria, purga ou acessório. Confirme a prévia no Bambu Studio.

## Formatos

- Fonte paramétrico: editável e reproduzível.
- STL: malha geométrica, sem perfil completo de impressão.
- STEP: geometria CAD editável/importável quando o modelador suportar.
- 3MF: contêiner de projeto; pode incluir peças, placas e configurações.
- G-code / 3MF fatiado: específico de impressora, bico, filamento, placa e perfil.

O Bambu Studio oficial importa STL/3MF e oferece fatiamento e prévia. A CLI documenta `--slice` e `--export-3mf`, mas só use comandos presentes na versão instalada.

Fontes oficiais:
- https://github.com/bambulab/BambuStudio
- https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage
